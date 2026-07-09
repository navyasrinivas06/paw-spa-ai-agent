async function loadBookings() {

    try {

        const response = await fetch("https://paw-spa-ai-agent.onrender.com/bookings");

        const bookings = await response.json();

        const tbody = document.querySelector("#bookingTable tbody");

        tbody.innerHTML = "";

        bookings.forEach((booking) => {

            tbody.innerHTML += `
                <tr>
                    <td>${booking.id}</td>
                    <td>${booking.name}</td>
                    <td>${booking.phone}</td>
                    <td>${booking.pet_name}</td>
                    <td>${booking.pet_type}</td>
                    <td>${booking.breed}</td>
                    <td>${booking.service}</td>
                    <td>${booking.date}</td>
                    <td>${booking.time}</td>
<td>
    <button onclick="deleteBooking(${booking.id})">
        Delete
    </button>
</td>
                </tr>
            `;

        });

    } catch (error) {

        console.error(error);
        alert("Unable to load bookings.");

    }

}

loadBookings();

async function deleteBooking(id) {

    if (!confirm("Delete this booking?")) {
        return;
    }

    try {

        const response = await fetch(
            `https://paw-spa-ai-agent.onrender.com/book/${id}`,
            {
                method: "DELETE"
            }
        );

        const data = await response.json();

        alert(data.message);

        loadBookings();

    } catch (error) {

        console.error(error);
        alert("Unable to delete booking.");

    }

}