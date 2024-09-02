from flask import Flask, request, jsonify, render_template
import random
import smtplib
import os
from email.message import EmailMessage

# Print the current working directory
print("Current Working Directory:", os.getcwd())

# Initialize the Flask app
app = Flask(__name__)

# Setup your email server credentials
sender_email = "manojkumargowd065@gmail.com"
password = "sjhzkhqbdwvkppmb"

# Setup and configure the email server 
server = smtplib.SMTP('smtp.gmail.com', 587)  # Connect to the Gmail SMTP server on port 587
server.starttls()  # Upgrade the connection to a secure encrypted  connection
server.login(sender_email, password)  # Login to the email server using the sender's credentials

# In-memory storage for OTPs (for demonstration purposes)
otp_storage = {}

# Route to serve the HTML page
@app.route('/')
def index():
    # Render the HTML page (webpage.html) when the root URL is accessed
    return render_template('webpage.html')

# Route to handle sending the OTP
@app.route('/send_otp', methods=['POST'])
def send_otp():
    # Get the data sent in the POST request (expecting JSON format)
    data = request.json
    name = data.get('name')  # Extract the user's name
    receiver_email = data.get('email')  # Extract the receiver's email
    
    # Validate the presence of both name and email in the request
    if not name or not receiver_email:
        return jsonify({'message': 'Name and email are required.'}), 400

    # OTP generation (6-digit OTP in this case)
    OTP = random.randint(100000, 999999)
    otp_storage[receiver_email] = OTP  # Store the OTP in the in-memory dictionary with the receiver's email as the key
    
    # Compose the email message
    subject = "OTP Verification Using Python"
    body = f"Dear {name},\n\nYour OTP is {OTP}."
    
    # Create the email message
    message = EmailMessage()
    message.set_content(body)  # Set the email body
    message['Subject'] = subject  # Set the email subject
    message['From'] = sender_email  # Set the sender's email
    message['To'] = receiver_email  # Set the receiver's email

    try:
        # Attempt to send the email
        server.send_message(message)
        return jsonify({'message': 'OTP sent successfully to ' + receiver_email})
    except Exception as e:
        # Handle any errors that occur during the email sending process
        return jsonify({'message': 'Failed to send OTP', 'error': str(e)}), 500

# Route to handle OTP verification
@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    # Get the data sent in the POST request (expecting JSON format)
    data = request.json
    receiver_email = data.get('email')  # Extract the receiver's email
    otp = data.get('otp')  # Extract the OTP entered by the user
    
    # Validate the presence of both email and OTP in the request
    if not receiver_email or not otp:
        return jsonify({'message': 'Email and OTP are required.'}), 400
    
    # Retrieve the stored OTP for the given email
    stored_otp = otp_storage.get(receiver_email)
    
    # Check if the stored OTP matches the one provided by the user
    if stored_otp and int(otp) == stored_otp:
        del otp_storage[receiver_email]  # Remove OTP from storage after successful verification
        return jsonify({'message': 'OTP verified successfully!'})
    else:
        return jsonify({'message': 'Invalid OTP or OTP expired.'}), 400

# Main entry point to run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
