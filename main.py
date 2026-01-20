from flask import Flask, request
import json
import os
from datetime import datetime

app = Flask(__name__)

ATTENDANCE_FILE = 'attendance.json'

def load_attendance():
    """Load attendance data from file"""
    try:
        if os.path.exists(ATTENDANCE_FILE):
            with open(ATTENDANCE_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_attendance(data):
    """Save attendance data to file"""
    with open(ATTENDANCE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    # Sample staff data
    staff_data = load_attendance()

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>👥 Staff Attendance System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .header h1 {
                color: #333;
                font-size: 2.5em;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 15px;
            }
            .date-time {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                margin: 20px 0;
                font-weight: bold;
                color: #666;
            }
            .attendance-form {
                background: #f8f9fa;
                padding: 25px;
                border-radius: 15px;
                margin: 25px 0;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
                color: #333;
            }
            input, select {
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
                box-sizing: border-box;
            }
            input:focus, select:focus {
                outline: none;
                border-color: #667eea;
            }
            .button-group {
                display: flex;
                gap: 15px;
                margin-top: 25px;
            }
            button {
                flex: 1;
                padding: 15px;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }
            .checkin-btn {
                background: #28a745;
                color: white;
            }
            .checkout-btn {
                background: #ffc107;
                color: #333;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .attendance-table {
                width: 100%;
                border-collapse: collapse;
                margin: 30px 0;
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .attendance-table th, .attendance-table td {
                border: 1px solid #ddd;
                padding: 15px;
                text-align: left;
            }
            .attendance-table th {
                background: #667eea;
                color: white;
            }
            .attendance-table tr:nth-child(even) {
                background: #f9f9f9;
            }
            .status-present {
                background: #d4edda;
                color: #155724;
                padding: 5px 10px;
                border-radius: 20px;
                font-weight: bold;
            }
            .status-absent {
                background: #f8d7da;
                color: #721c24;
                padding: 5px 10px;
                border-radius: 20px;
                font-weight: bold;
            }
            .status-onleave {
                background: #fff3cd;
                color: #856404;
                padding: 5px 10px;
                border-radius: 20px;
                font-weight: bold;
            }
            .empty-state {
                text-align: center;
                padding: 40px;
                color: #666;
                font-size: 1.2em;
            }
            .stats-box {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .stat-card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                border-top: 5px solid #667eea;
            }
            .stat-number {
                font-size: 2.5em;
                font-weight: bold;
                color: #667eea;
                margin: 10px 0;
            }
            .message {
                padding: 15px;
                border-radius: 10px;
                margin: 15px 0;
                text-align: center;
                font-weight: bold;
                display: none;
            }
            .success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
                display: block;
            }
            .error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
                display: block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>
                    <span>👥</span>
                    Staff Attendance System
                    <span>👥</span>
                </h1>
            </div>

            <div class="date-time" id="currentDateTime">
                Loading date and time...
            </div>

            <!-- Attendance Form -->
            <div class="attendance-form">
                <h2 style="color: #667eea; margin-bottom: 20px;">📝 Mark Attendance</h2>

                <form method="POST" action="/mark_attendance" id="attendanceForm">
                    <div class="form-group">
                        <label for="staff_id">Staff ID:</label>
                        <input type="text" id="staff_id" name="staff_id" placeholder="Enter Staff ID" required>
                    </div>

                    <div class="form-group">
                        <label for="staff_name">Staff Name:</label>
                        <input type="text" id="staff_name" name="staff_name" placeholder="Enter Staff Name" required>
                    </div>

                    <div class="form-group">
                        <label for="department">Department:</label>
                        <select id="department" name="department" required>
                            <option value="">Select Department</option>
                            <option value="IT">💻 IT Department</option>
                            <option value="HR">👥 HR Department</option>
                            <option value="Sales">💰 Sales Department</option>
                            <option value="Marketing">📢 Marketing Department</option>
                            <option value="Operations">🏢 Operations Department</option>
                            <option value="Finance">💵 Finance Department</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="status">Attendance Status:</label>
                        <select id="status" name="status" required>
                            <option value="">Select Status</option>
                            <option value="Present">✅ Present</option>
                            <option value="Late">⏰ Late</option>
                            <option value="Half Day">⏳ Half Day</option>
                            <option value="On Leave">🏖️ On Leave</option>
                            <option value="Absent">❌ Absent</option>
                        </select>
                    </div>

                    <div class="button-group">
                        <button type="submit" name="action" value="checkin" class="checkin-btn">
                            ✅ Check In
                        </button>
                        <button type="submit" name="action" value="checkout" class="checkout-btn">
                            🏃 Check Out
                        </button>
                    </div>
                </form>
            </div>

            <!-- Statistics -->
            <div class="stats-box" id="statsSection">
                <!-- Stats will be loaded by JavaScript -->
            </div>

            <!-- Attendance Records -->
            <div>
                <h2 style="color: #667eea; margin-bottom: 20px;">📊 Today's Attendance</h2>
                <div id="attendanceTable">
    '''

    # Load today's attendance
    today = datetime.now().strftime('%Y-%m-%d')
    if today in staff_data:
        html += '''
                    <table class="attendance-table">
                        <thead>
                            <tr>
                                <th>Staff ID</th>
                                <th>Name</th>
                                <th>Department</th>
                                <th>Check In</th>
                                <th>Check Out</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
        '''

        for record in staff_data[today]:
            status_class = {
                'Present': 'status-present',
                'Late': 'status-present',
                'Half Day': 'status-present',
                'On Leave': 'status-onleave',
                'Absent': 'status-absent'
            }.get(record.get('status', ''), '')

            html += f'''
                            <tr>
                                <td>{record.get('staff_id', '')}</td>
                                <td>{record.get('staff_name', '')}</td>
                                <td>{record.get('department', '')}</td>
                                <td>{record.get('checkin_time', '--:--')}</td>
                                <td>{record.get('checkout_time', '--:--')}</td>
                                <td><span class="{status_class}">{record.get('status', '')}</span></td>
                            </tr>
            '''

        html += '''
                        </tbody>
                    </table>
        '''
    else:
        html += '''
                    <div class="empty-state">
                        📭 No attendance records for today yet!
                    </div>
        '''

    html += '''
                </div>
            </div>

            <!-- Message Display -->
            <div id="message" class="message"></div>

            <div style="text-align: center; margin-top: 40px; color: #666; font-size: 0.9em;">
                <p>© Staff Attendance System | Made with Flask</p>
            </div>
        </div>

        <script>
            // Update current date and time
            function updateDateTime() {
                const now = new Date();
                const options = { 
                    weekday: 'long', 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                };
                document.getElementById('currentDateTime').textContent = 
                    '📅 ' + now.toLocaleDateString('en-US', options);
            }

            // Update stats
            async function updateStats() {
                try {
                    const response = await fetch('/get_stats');
                    const data = await response.json();

                    if (data.success) {
                        const statsBox = document.getElementById('statsSection');
                        statsBox.innerHTML = `
                            <div class="stat-card">
                                <div>👥 Total Staff</div>
                                <div class="stat-number">${data.total_staff}</div>
                                <div>Today</div>
                            </div>
                            <div class="stat-card">
                                <div>✅ Present</div>
                                <div class="stat-number">${data.present}</div>
                                <div>${data.present_percentage}%</div>
                            </div>
                            <div class="stat-card">
                                <div>⏰ Late</div>
                                <div class="stat-number">${data.late}</div>
                                <div>${data.late_percentage}%</div>
                            </div>
                            <div class="stat-card">
                                <div>❌ Absent</div>
                                <div class="stat-number">${data.absent}</div>
                                <div>${data.absent_percentage}%</div>
                            </div>
                        `;
                    }
                } catch (error) {
                    console.error('Error loading stats:', error);
                }
            }

            // Show message
            function showMessage(text, type) {
                const messageDiv = document.getElementById('message');
                messageDiv.textContent = text;
                messageDiv.className = `message ${type}`;

                // Auto-hide after 5 seconds
                setTimeout(() => {
                    messageDiv.style.display = 'none';
                }, 5000);
            }

            // Handle form submission
            document.getElementById('attendanceForm').addEventListener('submit', async function(e) {
                e.preventDefault();

                const formData = new FormData(this);
                const action = formData.get('action');

                try {
                    const response = await fetch('/mark_attendance', {
                        method: 'POST',
                        body: formData
                    });

                    const result = await response.text();

                    // Check if response contains success message
                    if (result.includes('success')) {
                        const match = result.match(/message=(.*?)&type=(.*?)'/);
                        if (match) {
                            const message = decodeURIComponent(match[1]);
                            const type = match[2];
                            showMessage(message, type);

                            // Refresh page after 2 seconds
                            setTimeout(() => {
                                location.reload();
                            }, 2000);
                        }
                    } else {
                        showMessage('❌ Error processing attendance!', 'error');
                    }
                } catch (error) {
                    showMessage('❌ Network error! Please try again.', 'error');
                    console.error('Error:', error);
                }
            });

            // Load stats when page loads
            window.onload = function() {
                updateDateTime();
                updateStats();

                // Update time every second
                setInterval(updateDateTime, 1000);

                // Update stats every 30 seconds
                setInterval(updateStats, 30000);

                // Show message from URL parameters
                const urlParams = new URLSearchParams(window.location.search);
                const message = urlParams.get('message');
                const messageType = urlParams.get('type');

                if (message) {
                    showMessage(decodeURIComponent(message), messageType);
                }
            };
        </script>
    </body>
    </html>
    '''

    return html

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    """Handle attendance marking"""
    try:
        staff_id = request.form.get('staff_id', '').strip()
        staff_name = request.form.get('staff_name', '').strip()
        department = request.form.get('department', '').strip()
        status = request.form.get('status', '').strip()
        action = request.form.get('action', 'checkin')

        # Validate inputs
        if not all([staff_id, staff_name, department, status]):
            message = "❌ Please fill all fields!"
            return f'<script>window.location.href="/?message={message}&type=error";</script>'

        # Load existing attendance
        attendance_data = load_attendance()
        today = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M')

        # Initialize today's records if not exists
        if today not in attendance_data:
            attendance_data[today] = []

        # Check if staff already marked attendance today
        existing_record = None
        for record in attendance_data[today]:
            if record['staff_id'] == staff_id:
                existing_record = record
                break

        if action == 'checkin':
            if existing_record:
                message = f"❌ {staff_name} already checked in today!"
                return f'<script>window.location.href="/?message={message}&type=error";</script>'

            # Add new check-in record
            attendance_data[today].append({
                'staff_id': staff_id,
                'staff_name': staff_name,
                'department': department,
                'status': status,
                'checkin_time': current_time,
                'checkout_time': '--:--',
                'date': today
            })

            message = f"✅ {staff_name} checked in successfully at {current_time}!"

        elif action == 'checkout':
            if not existing_record:
                message = f"❌ {staff_name} hasn't checked in today!"
                return f'<script>window.location.href="/?message={message}&type=error";</script>'

            if existing_record['checkout_time'] != '--:--':
                message = f"❌ {staff_name} already checked out today!"
                return f'<script>window.location.href="/?message={message}&type=error";</script>'

            # Update checkout time
            existing_record['checkout_time'] = current_time
            message = f"✅ {staff_name} checked out successfully at {current_time}!"

        # Save attendance data
        save_attendance(attendance_data)

        return f'<script>window.location.href="/?message={message}&type=success";</script>'

    except Exception as e:
        message = f"❌ Error: {str(e)}"
        return f'<script>window.location.href="/?message={message}&type=error";</script>'

@app.route('/get_stats')
def get_stats():
    """Get attendance statistics"""
    try:
        attendance_data = load_attendance()
        today = datetime.now().strftime('%Y-%m-%d')

        if today not in attendance_data:
            return {
                'success': True,
                'total_staff': 0,
                'present': 0,
                'late': 0,
                'absent': 0,
                'present_percentage': 0,
                'late_percentage': 0,
                'absent_percentage': 0
            }

        today_records = attendance_data[today]
        total_staff = len(today_records)

        # Count statuses
        present = sum(1 for r in today_records if r['status'] in ['Present', 'Late', 'Half Day'])
        late = sum(1 for r in today_records if r['status'] == 'Late')
        absent = sum(1 for r in today_records if r['status'] == 'Absent')

        # Calculate percentages
        present_percentage = round((present / total_staff) * 100, 1) if total_staff > 0 else 0
        late_percentage = round((late / total_staff) * 100, 1) if total_staff > 0 else 0
        absent_percentage = round((absent / total_staff) * 100, 1) if total_staff > 0 else 0

        return {
            'success': True,
            'total_staff': total_staff,
            'present': present,
            'late': late,
            'absent': absent,
            'present_percentage': present_percentage,
            'late_percentage': late_percentage,
            'absent_percentage': absent_percentage
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)