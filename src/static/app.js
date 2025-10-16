document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";
      
      // Clear existing options (except the first default option)
      activitySelect.innerHTML = '<option value="">Select an activity</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        // Create participants list
        const participantsList = details.participants.length > 0 
          ? `<ul class="activity-card__participants-list">${details.participants.map(email => 
              `<li class="activity-card__participant">
                 <span class="activity-card__participant-email">${email}</span>
                 <button class="activity-card__delete-btn" data-activity="${name}" data-email="${email}" title="Remove participant">✕</button>
               </li>`
            ).join('')}</ul>`
          : '<p class="activity-card__no-participants">No participants yet</p>';

        activityCard.innerHTML = `
          <h4 class="activity-card__title">${name}</h4>
          <p class="activity-card__text">${details.description}</p>
          <p class="activity-card__text"><strong>Schedule:</strong> ${details.schedule}</p>
          <p class="activity-card__text"><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="activity-card__participants">
            <p class="activity-card__participants-title"><strong>Current Participants:</strong></p>
            ${participantsList}
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });

      // Add event listeners for delete buttons
      document.querySelectorAll('.activity-card__delete-btn').forEach(button => {
        button.addEventListener('click', handleDeleteParticipant);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Function to handle participant deletion
  async function handleDeleteParticipant(event) {
    const button = event.target;
    const activity = button.getAttribute('data-activity');
    const email = button.getAttribute('data-email');

    if (!confirm(`Are you sure you want to remove ${email} from ${activity}?`)) {
      return;
    }

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
        }
      );

      const result = await response.json();

      if (response.ok) {
        displayMessage(result.message, true);
        // Refresh the activities list
        await fetchActivities();
      } else {
        displayMessage(result.detail || "An error occurred", false);
      }
    } catch (error) {
      displayMessage("Failed to remove participant. Please try again.", false);
      console.error("Error removing participant:", error);
    }
  }

  // Function to display message and auto-hide after 5 seconds
  function displayMessage(text, isSuccess = true) {
    messageDiv.textContent = text;
    messageDiv.className = isSuccess ? "message message--success" : "message message--error";
    messageDiv.classList.remove("message--hidden");

    // Hide message after 5 seconds
    setTimeout(() => {
      messageDiv.classList.add("message--hidden");
    }, 5000);
  }

  // Function to handle form submission
  async function handleFormSubmission(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        displayMessage(result.message, true);
        signupForm.reset();
        // Refresh the activities list to show the new participant
        await fetchActivities();
      } else {
        displayMessage(result.detail || "An error occurred", false);
      }
    } catch (error) {
      displayMessage("Failed to sign up. Please try again.", false);
      console.error("Error signing up:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", handleFormSubmission);

  // Initialize app
  fetchActivities();
});
