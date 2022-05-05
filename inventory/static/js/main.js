document.addEventListener("DOMContentLoaded", () => {

    const computerButton = document.querySelector("#computer");
    const inventoryButton = document.querySelector("#inventory");
    const salesButton = document.querySelector("#sales");
    const financesButton = document.querySelector("#finances");

    computerButton.onclick = () => loadComputer();
    inventoryButton.onclick = () => loadInventory();
    salesButton.onclick = () => loadSales();
    financesButton.onclick = () => loadFinances();

    // By default, load the computer
    loadComputer();

    // Page-history features
    window.onpopstate = event => {
        window[`load${event.state.section}`](pop = false);
    }

    // Add the part then load inventory
    document.querySelector("#new-part").onsubmit = () => {
        const partName = document.querySelector("#part_name").value;
        const quantity = document.querySelector("#quantity").value;
        const unitPrice = document.querySelector("#unit_price").value;
        addPart(partName, quantity, unitPrice);
        return false;
    }

    // Add a sale then load sales
    document.querySelector("#new-sale").onsubmit = () => {
        const saledItem = document.querySelector("#saled_item").value;
        const dateTime = document.querySelector("#date_time").value;
        addSale(saledItem, dateTime);
        return false;
    }
})

function loadComputer(pop = true) {
    fetch("app/computer")
        .then(response => response.json())
        .then(data => {
            document.querySelector("#inventory-view").style.display = "none";
            document.querySelector("#sales-view").style.display = "none";
            document.querySelector("#finances-view").style.display = "none";
            document.querySelector("#details-view").style.display = "none";
            const computer = document.querySelector("#computer-view");
            computer.innerHTML = "";
            computer.style.display = "flex";
            computer.style.flexWrap = "wrap";
            computer.style.justifyContent = "space-between";
            computer.style.gap = "10px";
            let itemForm = document.createElement("form");
            itemForm.method = "POST";
            itemForm.id = "new-item";
            itemForm.action = "/new_item/"
            itemForm.innerHTML = `
            <input required type="text" name="item_name" placeholder="Name">
            <input required type="number" name="price" placeholder="Price">
            <input required type="url" name="image_url" placeholder="Image URL">
            <input required type="url" name="details_url" placeholder="Details URL">
            <button type="submit">Add</button>
        `;
            computer.append(itemForm);
            JSON.parse(data).forEach(result => {
                let details = document.createElement("div");
                details.className = "card";
                details.style.width = "15rem";
                details.innerHTML = `
                <img src="${result.details_image}" class="card-img-top" alt="">
                <div class="card-body">
                    <h5 class="card-title">${result.name}</h5>
                    <h6 class="card-subtitle my-2 text-success">Rs ${result.price}</h6>
                    <a class="details-button btn my-4" href="${result.details_link}" style="width: 100%">View Details</a>
                </div>
            `;
                computer.append(details);
            })
            if (pop) history.pushState({ section: "Computer" }, "", "#computer");
        })
        .catch(error => console.log(error))
}

function loadInventory(pop = true) {
    fetch("app/inventory")
        .then(response => response.json())
        .then(data => {
            const parts = document.querySelector("#inventory-view > ul");
            parts.innerHTML = "";
            document.getElementById("new-part").reset();
            document.querySelector("#computer-view").style.display = "none";
            document.querySelector("#sales-view").style.display = "none";
            document.querySelector("#finances-view").style.display = "none";
            document.querySelector("#details-view").style.display = "none";
            document.querySelector("#inventory-view").style.display = "block";
            JSON.parse(data).forEach(result => {
                let part = document.createElement("li");
                part.innerHTML = `<strong>${result.name}</strong> | <em>${result.quantity} in stock</em> | <span class="text-success">Rs ${result.unit_price}</span>`;
                let deleteButton = document.createElement("button");
                deleteButton.className = "del-button";
                deleteButton.innerHTML = "Delete";
                deleteButton.addEventListener("click", () => deletePart(part, result.id));
                part.append(deleteButton);
                parts.append(part);
            })
            if (pop) history.pushState({ section: "Inventory" }, "", "#inventory");
        })
        .catch(error => console.log(error));
}

function loadSales(pop = true) {
    fetch("app/sales")
        .then(response => response.json())
        .then(data => {
            const sales = document.querySelector("#sales-view > ul");
            sales.innerHTML = "";
            document.getElementById("new-sale").reset();
            document.querySelector("#computer-view").style.display = "none";
            document.querySelector("#inventory-view").style.display = "none";
            document.querySelector("#finances-view").style.display = "none";
            document.querySelector("#details-view").style.display = "none";
            document.querySelector("#sales-view").style.display = "block";
            data.forEach(result => {
                let sale = document.createElement("li");
                sale.innerHTML = `<strong>${result.computer_item}</strong> was saled on ${result.timestamp}`;
                sales.append(sale);
            })
            if (pop) history.pushState({ section: "Sales" }, "", "#sales");
        })
        .catch(error => console.log(error))
}

function loadFinances(pop = true) {
    fetch("app/finances")
        .then(response => response.json())
        .then(data => {
            document.querySelector("#computer-view").style.display = "none";
            document.querySelector("#inventory-view").style.display = "none";
            document.querySelector("#sales-view").style.display = "none";
            document.querySelector("#details-view").style.display = "none";
            document.querySelector("#finances-view").style.display = "flex";
            document.querySelector("#profit > h2").innerHTML = `Rs ${data.profit}`;
            document.querySelector("#revenue > h2").innerHTML = `Rs ${data.revenue}`;
            // document.querySelector("#expenses_item > h2").innerHTML = `Rs ${data.expenses_item}`;
            document.querySelector("#expenses > h2").innerHTML = `Rs ${data.expenses}`;
            if (pop) history.pushState({ section: "Finances" }, "", "#finances");
        })
        .catch(error => console.log(error))
}

function addPart(partName, quantity, unitPrice) {
    fetch("new_part/", {
            method: "POST",
            body: JSON.stringify({
                part_name: partName,
                quantity: quantity,
                unit_price: unitPrice
            })
        })
        .then(response => response.json())
        .then(result => {
            if (!("error" in result)) loadInventory();
        })
        .catch(error => console.log(error))
}

function deletePart(part, partId) {
    fetch("delete_part/", {
            method: "PUT",
            body: JSON.stringify({
                part_id: partId,
                remove: true
            })
        })
        .then(response => response.json())
        .then(result => {
            if (!("error" in result)) part.remove();
        })
        .catch(error => console.log(error))
}

function addSale(saledItem, dateTime) {
    fetch("new_sale/", {
            method: "POST",
            body: JSON.stringify({
                saled_item: saledItem,
                date_time: dateTime,
            })
        })
        .then(response => response.json())
        .then(result => {
            if (!("error" in result)) loadSales();
        })
        .catch(error => console.log(error))
}