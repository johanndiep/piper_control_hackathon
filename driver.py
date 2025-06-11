from piper_control import piper_control
import numpy as np


class PiperArmController:
    """
    A controller class for interfacing with the Piper robotic arm using the piper_control API.
    It allows joint angle control, gripper manipulation, and interactive terminal input for easy use.
    """

    def __init__(self, can_port="can0"):
        """
        Initializes the PiperArmController object by connecting to the robot through the specified CAN port.
        Also defines the start position and gripper open/closed constants.
        
        Parameters:
        - can_port (str): The CAN port used to communicate with the robot.
        """
        self.robot = piper_control.PiperControl(can_port=can_port)
        self.robot.reset()  # Ensure the robot is in a clean state
        self.start_position = np.array([-1.593, 0.634, -0.286, 0, 0.385, -1.85])  # Default start joint configuration
        self.current_position = self.start_position.copy()
        self.GRIPPER_OPEN = 0.07  # Max gripper open width (meters)
        self.GRIPPER_CLOSED = 0.0  # Gripper closed position

    def set_start_position(self):
        """
        Moves the robot arm to the predefined start position.
        """
        self._set_joint_positions(self.start_position)
    
    def set_relative_angles(self, angle_differences):
        """
        Moves the robot arm by a relative offset from the start position.
        
        Parameters:
        - angle_differences (np.ndarray): Array of angle changes to apply to the start position.
        """
        target_angles = self.start_position + np.array(angle_differences)
        self._set_joint_positions(target_angles)

    def get_joint_angles(self):
        """
        Returns the current joint angles in radians, rounded to 3 decimal places.
        
        Returns:
        - np.ndarray: Joint angles (radians)
        """
        return np.round(self.robot.get_joint_positions(), 3)

    def get_joint_angles_degrees(self):
        """
        Returns the current joint angles in degrees, rounded to 1 decimal place.
        
        Returns:
        - np.ndarray: Joint angles (degrees)
        """
        return np.round(np.degrees(self.get_joint_angles()), 1)

    def get_relative_angles(self):
        """
        Returns the current joint angles relative to the predefined start position in radians.
        
        Returns:
        - np.ndarray: Relative joint angles (radians)
        """
        current = self.get_joint_angles()
        return np.round(current - self.start_position, 3)

    def get_relative_angles_degrees(self):
        """
        Returns the relative joint angles in degrees.
        
        Returns:
        - np.ndarray: Relative joint angles (degrees)
        """
        return np.round(np.degrees(self.get_relative_angles()), 1)

    def _set_joint_positions(self, angles):
        """
        Sends a command to move the robot joints to specific angles.
        
        Parameters:
        - angles (np.ndarray): Target joint angles (radians)
        """
        self.robot.set_joint_positions(angles)
        self.current_position = np.array(angles).copy()

    def reset_to_zero_position(self):
        """
        Moves the robot arm to a neutral position with all joint angles set to zero.
        """
        zero_position = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self._set_joint_positions(zero_position)

    def get_gripper_state(self):
        """
        Retrieves the normalized gripper opening between 0 (closed) and 1 (fully open).
        
        Returns:
        - float: Normalized gripper position
        """
        actual_position, _ = self.robot.get_gripper_state()
        return np.clip(actual_position / self.GRIPPER_OPEN, 0.0, 1.0)

    def set_gripper(self, position: float):
        """
        Sets the gripper opening based on a normalized value between 0 and 1.
        
        Parameters:
        - position (float): Gripper open amount (0 = closed, 1 = open)
        """
        actual_position = np.clip(position, 0.0, 1.0) * self.GRIPPER_OPEN
        self.robot.set_gripper_ctrl(position=actual_position)

    def interactive_control(self):
        """
        Runs an interactive terminal-based control loop for controlling the robot arm and gripper.
        Users can input joint angles in radians/degrees, switch between absolute and relative control,
        and control the gripper through simple commands.
        """
        while True:
            # Display current robot state
            print("\nCurrent state:")
            print(f"Joints (rad): {self.get_joint_angles()}")
            print(f"Joints (deg): {self.get_joint_angles_degrees()}")
            print(f"Relative to start (rad): {self.get_relative_angles()}")
            print(f"Gripper position: {self.get_gripper_state():.2f} (0=closed, 1=open)")
            
            # Prompt user for input
            user_input = input(
                "Enter joint angles (prefix + for relative, suffix d for degrees)\n"
                "or 'g' for gripper control, 'q' to quit: ").strip()
            
            if user_input.lower() in ['q', 'quit', 'exit']:
                break  # Exit control loop
            elif user_input.lower() == 'g':
                self._handle_gripper_input()  # Delegate to gripper control handler
            else:
                try:
                    # Check if angles are specified in degrees
                    degrees_mode = user_input.lower().endswith('d')
                    clean_input = user_input[:-1].strip() if degrees_mode else user_input
                    
                    # Check if angles are specified relatively
                    relative_mode = clean_input.startswith('+')
                    if relative_mode:
                        numbers_part = clean_input[1:].strip()
                        if numbers_part.startswith('-'):
                            numbers_input = numbers_part
                        else:
                            numbers_input = numbers_part
                    else:
                        numbers_input = clean_input
                    
                    # Parse the input into a numpy array
                    angles = np.fromstring(numbers_input, sep=' ')
                    
                    if degrees_mode:
                        angles = np.radians(angles)  # Convert degrees to radians
                    
                    angles = np.round(angles, 3)  # Round to 3 decimals
                    
                    if relative_mode:
                        self.set_relative_angles(angles)
                    else:
                        self._set_joint_positions(angles)
                        
                except Exception as e:
                    # Handle input errors and show examples
                    print(f"Invalid input: {str(e)}")
                    print("Example valid inputs:")
                    print("Absolute radians: 1.0 -0.5 0.3 0.2 -1.2 0.8")
                    print("Absolute degrees: 45 -30 15 10 -70 45d")
                    print("Relative radians: +0.1 0 -0.2 0 0.3 0")
                    print("Relative degrees: +5 0 -10 0 15 0d")
                    print("Relative with negative: +-0.1 0 -0.2 0 0.3 0")

    def _handle_gripper_input(self):
        """
        Subroutine to manage gripper control interactively.
        Allows opening, closing, or setting the gripper to a specific normalized position.
        """
        while True:
            current = self.get_gripper_state()
            print(f"\nCurrent gripper: {current:.2f} (0=closed, 1=open)")
            print("Commands: o=open, c=close, 0-1=position, b=back")
            
            gripper_input = input("Gripper command: ").strip().lower()
            
            if gripper_input == 'b':
                break  # Exit gripper control
            elif gripper_input == 'o':
                self.set_gripper(1.0)
                print("Gripper opened fully")
            elif gripper_input == 'c':
                self.set_gripper(0.0)
                print("Gripper closed fully")
            else:
                try:
                    position = float(gripper_input)
                    if 0 <= position <= 1:
                        self.set_gripper(position)
                        print(f"Gripper set to {position:.2f}")
                    else:
                        print("Position must be between 0 and 1")
                except ValueError:
                    print("Invalid input. Enter number 0-1 or o/c/b")


if __name__ == "__main__":
    # Example script run
    arm = PiperArmController()
    arm.set_start_position()
    print(f"Start position (rad): {arm.get_joint_angles()}")
    print(f"Start position (deg): {arm.get_joint_angles_degrees()}")
    arm.interactive_control()
