from flask import Flask, render_template, request
from datetime import datetime, timedelta

# Tell Flask where to find templates and static files
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    # static_folder="../frontend/static"
)

@app.route("/", methods=["GET", "POST"])
def planner():
    if request.method == "POST":
        # 1️⃣ Get form data
        wake_time_str = request.form.get("wake_time")  # "HH:MM"
        study_hours = float(request.form.get("study"))
        travel_hours = float(request.form.get("travel"))
        task = request.form.get("task")

        # 2️⃣ Convert wake time to datetime
        wake_time = datetime.strptime(wake_time_str, "%H:%M")

        # 3️⃣ Prepare schedule
        schedule = []

        # Sleep time (assuming 8 hours)
        sleep_end = wake_time
        schedule.append(f"Wake up at {wake_time.strftime('%H:%M')}")

        # Study period
        study_end = wake_time + timedelta(hours=study_hours)
        schedule.append(f"Study from {wake_time.strftime('%H:%M')} to {study_end.strftime('%H:%M')}")

        # Travel period
        travel_end = study_end + timedelta(hours=travel_hours)
        schedule.append(f"Travel from {study_end.strftime('%H:%M')} to {travel_end.strftime('%H:%M')}")

        # Task period (assume 2 hours)
        task_end = travel_end + timedelta(hours=2)
        schedule.append(f"Do task '{task}' from {travel_end.strftime('%H:%M')} to {task_end.strftime('%H:%M')}")

        # Free time
        total_hours = 24
        sleep_hours = 8
        freetime_hours = total_hours - sleep_hours - study_hours - travel_hours - 2
        if freetime_hours > 0:
            schedule.append(f"Free time for {freetime_hours} hours")

        return render_template(
            "./planner.html",
            wake_time=wake_time_str,
            study=study_hours,
            travel=travel_hours,
            task=task,
            schedule=schedule
        )

    # GET request
    return render_template(
        "planner.html",
        wake_time="07:00",
        study="",
        travel="",
        task="",
        schedule=None
    )

if __name__ == "__main__":
    app.run(debug=True)
