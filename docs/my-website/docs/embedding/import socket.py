import socket
import time
import numpy as np
import matplotlib.pyplot as plt

# Constants
SERVER_IP = '192.168.1.10'  # IP address of the spacecraft (or simulator)
SERVER_PORT = 5000          # Port for communication
BUFFER_SIZE = 1024          # Size of buffer for receiving data

# Telemetry data simulation (in real cases, the data will be sent by spacecraft)
def simulate_telemetry():
    """
    Simulates telemetry data sent by the spacecraft.
    This function can be replaced by actual RF signal reception code.
    """
    # Simulating telemetry data (e.g., battery voltage, temperature)
    battery_voltage = np.random.uniform(10, 15)  # Random battery voltage between 10V and 15V
    temperature = np.random.uniform(-40, 100)    # Random temperature between -40°C and 100°C
    return {'battery_voltage': battery_voltage, 'temperature': temperature}

# Establish connection to spacecraft (Ground station communication)
def create_connection():
    """
    Creates a TCP connection to the spacecraft.
    """
    try:
        # Creating a socket connection to the spacecraft
        ground_station_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ground_station_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to spacecraft at {SERVER_IP}:{SERVER_PORT}")
        return ground_station_socket
    except Exception as e:
        print(f"Error connecting to spacecraft: {e}")
        return None

# Send commands to spacecraft
def send_command(ground_station_socket, command):
    """
    Sends a command to the spacecraft.
    """
    try:
        ground_station_socket.sendall(command.encode('utf-8'))
        print(f"Command sent: {command}")
    except Exception as e:
        print(f"Error sending command: {e}")

# Receive telemetry data from spacecraft
def receive_telemetry(ground_station_socket):
    """
    Receives telemetry data from the spacecraft.
    """
    try:
        data = ground_station_socket.recv(BUFFER_SIZE)
        if data:
            # Convert received data (assumed to be in JSON or similar format)
            print(f"Telemetry received: {data.decode('utf-8')}")
            return data.decode('utf-8')
        else:
            print("No data received.")
            return None
    except Exception as e:
        print(f"Error receiving telemetry: {e}")
        return None

# Process telemetry data (For visualization or analysis)
def process_telemetry_data(telemetry_data):
    """
    Process and visualize telemetry data.
    """
    # For the purpose of this example, let's assume the data is a dictionary
    telemetry_dict = eval(telemetry_data)
    
    # Plotting the telemetry data (Battery Voltage vs Temperature)
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(telemetry_dict['battery_voltage'], label="Battery Voltage (V)")
    plt.title("Spacecraft Telemetry")
    plt.xlabel("Time")
    plt.ylabel("Battery Voltage (V)")
    
    plt.subplot(2, 1, 2)
    plt.plot(telemetry_dict['temperature'], label="Temperature (C)", color='orange')
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.show()

# Main loop
def main():
    # Create socket connection to spacecraft (in real scenarios, this would be an RF receiver interface)
    ground_station_socket = create_connection()

    if not ground_station_socket:
        print("Failed to connect to spacecraft. Exiting.")
        return

    try:
        # Infinite loop to simulate telemetry reception and command sending
        while True:
            # Receive telemetry data from spacecraft
            telemetry_data = receive_telemetry(ground_station_socket)
            if telemetry_data:
                process_telemetry_data(telemetry_data)
            
            # Simulate sending a command to the spacecraft every 10 seconds
            command = "SET_ORBIT_POSITION"
            send_command(ground_station_socket, command)

            time.sleep(10)  # Wait for 10 seconds before next loop
    except KeyboardInterrupt:
        print("Exiting ground station simulation...")
    finally:
        ground_station_socket.close()

if __name__ == '__main__':
    main()
