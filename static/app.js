const qs = (s) => document.querySelector(s);
const qsa = (s) => document.querySelectorAll(s);

let selectedSlot = null;

// Generic API helper
async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || res.statusText);
  return data;
}

document.addEventListener("DOMContentLoaded", () => {
  const btnCheck = qs("#btnCheck");
  const btnBook = qs("#btnBook");
  if (btnCheck) btnCheck.onclick = checkAvailability;
  if (btnBook) btnBook.onclick = bookSlot;
  refreshMyBookings();
});

// --- Generate slots (client-side for demo) ---
async function checkAvailability() {
  const fid = qs("#facilitySelect").value;
  const date = qs("#dateInput").value;
  const grid = qs("#slotsGrid");
  grid.innerHTML = "";

  if (!date) return alert("Please select a date.");

  const start = 6;
  const end = 20;
  for (let h = start; h < end; h++) {
    const t = `${String(h).padStart(2, "0")}:00`;
    const b = document.createElement("button");
    b.className = "slot free";
    b.textContent = t;
    b.onclick = () => {
      qsa(".slot").forEach((x) => x.classList.remove("selected"));
      b.classList.add("selected");
      selectedSlot = t;
      qs("#btnBook").disabled = false;
    };
    grid.appendChild(b);
  }
}

// --- Booking ---
async function bookSlot() {
  if (!selectedSlot) return alert("Please select a time slot first.");

  const payload = {
    facility_id: qs("#facilitySelect").value,
    date: qs("#dateInput").value,
    start_time: selectedSlot,
    need_equipment: qs("#equipCheck").checked,
  };

  try {
    await api("/api/book", { method: "POST", body: JSON.stringify(payload) });
    showConfirmation();
    qs("#btnBook").disabled = true;
    selectedSlot = null;
    await refreshMyBookings();
  } catch (err) {
    alert(err.message);
  }
}

// --- Confirmation message ---
function showConfirmation() {
  const msg = qs("#confirmationMessage");
  msg.classList.remove("hidden");
  msg.classList.add("visible");
  msg.textContent = "✅ Your booking has been confirmed successfully!";
  setTimeout(() => msg.classList.add("hidden"), 4000);
}

// --- My Bookings List ---
async function refreshMyBookings() {
  const box = qs("#myBookings");
  try {
    const res = await fetch("/api/my-bookings");
    if (!res.ok) throw new Error("Unable to load bookings");
    const data = await res.json();
    if (!data.bookings || data.bookings.length === 0) {
      box.innerHTML = "<p>No bookings found.</p>";
      return;
    }
    box.innerHTML = data.bookings
      .map(
        (b) => `
      <div class="card small">
        <strong>${b.facility}</strong><br>
        ${b.date} at ${b.start_time}
        ${b.need_equipment ? "<br><em>Equipment issued</em>" : ""}
      </div>`
      )
      .join("");
  } catch {
    box.innerHTML = "<p class='error'>Error loading bookings.</p>";
  }
}
