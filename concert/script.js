const targetDate = new Date("2026-06-03T18:30:00");
const countdownRoot = document.getElementById("countdown");
const countdownEnded = document.getElementById("countdown-ended");
const copyButton = document.getElementById("copy-details");
const rowButtons = document.querySelectorAll(".row-button");
const concertRows = document.querySelectorAll(".concert-row");
const rowResult = document.getElementById("row-result");

const eventSummary = [
  "June Band Concert",
  "Wednesday, June 3, 2026, 6:30-8:00 PM",
  "Concert begins earlier than usual",
  "Chinook main gym",
  "Student arrival: 6:15-6:25 PM",
  "Students sit with parents or family when not performing",
  "Performance order: Heavy Metal, Jazz 2, Jazz 1, intermission, Entry, Intermediate, Advanced",
].join(" | ");

function pad(value) {
  return String(value).padStart(2, "0");
}

function updateCountdown() {
  const remaining = targetDate.getTime() - Date.now();

  if (remaining <= 0) {
    countdownRoot.hidden = true;
    countdownEnded.hidden = false;
    return;
  }

  const days = Math.floor(remaining / (1000 * 60 * 60 * 24));
  const hours = Math.floor((remaining / (1000 * 60 * 60)) % 24);
  const minutes = Math.floor((remaining / (1000 * 60)) % 60);
  const seconds = Math.floor((remaining / 1000) % 60);
  const values = [days, hours, minutes, seconds];

  countdownRoot.querySelectorAll("strong").forEach((cell, index) => {
    cell.textContent = pad(values[index]);
  });
}

if (countdownRoot && countdownEnded) {
  updateCountdown();
  window.setInterval(updateCountdown, 1000);
}

document.querySelectorAll(".reveal").forEach((element, index) => {
  element.style.animationDelay = `${index * 75}ms`;
});

rowButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const row = button.dataset.row;
    const chairs = button.dataset.chairs;
    const position = row === "1" ? "Front row" : `Row ${row}`;

    rowButtons.forEach((rowButton) => {
      rowButton.classList.toggle("active", rowButton === button);
    });
    concertRows.forEach((concertRow) => {
      concertRow.classList.toggle("active", concertRow.id === `row-${row}`);
    });

    rowResult.innerHTML = `<strong>${position}:</strong> ${chairs} chairs and ${chairs} stands.`;
  });
});

if (copyButton) {
  copyButton.addEventListener("click", async () => {
    const originalLabel = copyButton.textContent;

    try {
      await navigator.clipboard.writeText(eventSummary);
      copyButton.textContent = "Details copied";
    } catch {
      copyButton.textContent = "Unable to copy";
    }

    window.setTimeout(() => {
      copyButton.textContent = originalLabel;
    }, 1800);
  });
}
