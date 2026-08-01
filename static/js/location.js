let locationData = {};

const country = document.getElementById("country");
const admin1 = document.getElementById("admin1");
const admin2 = document.getElementById("admin2");

fetch("/static/data/location_data.json")
.then(response => response.json())
.then(data => {

    locationData = data;

    // Populate Country
    Object.keys(locationData).forEach(c => {

        country.innerHTML += `<option value="${c}">${c}</option>`;

    });

    // Restore Country if available
    const selectedCountry = country.dataset.selected;

    if(selectedCountry){

        country.value = selectedCountry;
        country.dispatchEvent(new Event("change"));

    }

});

country.addEventListener("change", function(){

    admin1.innerHTML = "<option value=''>Select Admin 1</option>";
    admin2.innerHTML = "<option value=''>Select Admin 2</option>";

    const selected = this.value;

    if(!selected) return;

    Object.keys(locationData[selected]).forEach(a1 => {

        admin1.innerHTML += `<option value="${a1}">${a1}</option>`;

    });

    // Restore Admin1 if available
    const selectedAdmin1 = admin1.dataset.selected;

    if(selectedAdmin1){

        admin1.value = selectedAdmin1;
        admin1.dispatchEvent(new Event("change"));

    }

});

admin1.addEventListener("change", function(){

    admin2.innerHTML = "<option value=''>Select Admin 2</option>";

    const selectedCountry = country.value;
    const selectedAdmin1 = this.value;

    if(!selectedCountry || !selectedAdmin1) return;

    locationData[selectedCountry][selectedAdmin1].forEach(a2 => {

        admin2.innerHTML += `<option value="${a2}">${a2}</option>`;

    });

    // Restore Admin2 if available
    const selectedAdmin2 = admin2.dataset.selected;

    if(selectedAdmin2){

        admin2.value = selectedAdmin2;

    }

});