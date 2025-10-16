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

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        // Create participants list
        const participantsList = details.participants.length > 0 
          ? `<ul class="activity-card__participants-list">${details.participants.map(email => `<li class="activity-card__participant">${email}</li>`).join('')}</ul>`
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
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
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
        messageDiv.textContent = result.message;
        messageDiv.className = "message message--success";
        signupForm.reset();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "message message--error";
      }

      messageDiv.classList.remove("message--hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("message--hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "message message--error";
      messageDiv.classList.remove("message--hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
