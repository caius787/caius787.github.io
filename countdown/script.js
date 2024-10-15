// Countdown logic for various dates

// Helper function to calculate time difference and display it, including years if needed
function updateCountdown(elementId, targetDate) {
    const now = new Date();
    const timeDifference = targetDate - now;

    let days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    let years = 0;

    // Check if the countdown exceeds a year and calculate years and days accordingly
    if (days > 365) {
        years = Math.floor(days / 365);
        days = days % 365;
    }

    const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

    // Create HTML structure for each countdown unit
    let countdownText = '';
    if (years > 0) {
        countdownText += `
        <div class="countdown-item">
            <div>${years.toString().padStart(2, '0')}</div>
            <h7>Years</h7>
        </div>`;
    }
    countdownText += `
    <div class="countdown-item">
        <div>${days.toString().padStart(2, '0')}</div>
        <h7>Days</h7>
    </div>
    <div class="countdown-item">
        <div>${hours.toString().padStart(2, '0')}</div>
        <h7>Hours</h7>
    </div>
    <div class="countdown-item">
        <div>${minutes.toString().padStart(2, '0')}</div>
        <h7>Minutes</h7>
    </div>
    <div class="countdown-item">
        <div>${seconds.toString().padStart(2, '0')}</div>
        <h7>Seconds</h7>
    </div>`;

    document.getElementById(elementId).innerHTML = countdownText;
}

// Initialize all countdowns
function startCountdowns() {
    // Countdown to October 31, 00:00
    const halloween = new Date(`${new Date().getFullYear()}-10-31T00:00:00`);
    if (new Date() > halloween) halloween.setFullYear(halloween.getFullYear() + 1);
    updateCountdown('countdown1', halloween);

    // Countdown to December 25, 00:00
    const christmas = new Date(`${new Date().getFullYear()}-12-25T00:00:00`);
    updateCountdown('countdown2', christmas);

    // Countdown to March 13, 00:00
    const march13 = new Date(`${new Date().getFullYear()}-03-13T00:00:00`);
    if (new Date() > march13) march13.setFullYear(march13.getFullYear() + 1);
    updateCountdown('countdown3', march13);

    // Countdown to March 13, 2029, 00:00
    const march13_2029 = new Date(`2029-03-13T00:00:00`);
    updateCountdown('countdown4', march13_2029);

    // Countdown to January 1, 00:00
    const jan1 = new Date(`${new Date().getFullYear() + 1}-01-01T00:00:00`);
    updateCountdown('countdown5', jan1);

    // Countdown to January 1, Leap Year