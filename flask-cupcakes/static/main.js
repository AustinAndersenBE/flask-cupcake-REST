function appendCupcake(cupcake) {
    const cupcakeList = document.getElementById("cupcakes");
    const newCupcake = document.createElement("li");


    const cupcakeDetails = document.createElement("div");
    const detailsText = document.createTextNode(`${cupcake.flavor} ${cupcake.size} ${cupcake.rating}`);
    cupcakeDetails.appendChild(detailsText);


    //delete button
    const deleteButton = document.createElement("button");
    deleteButton.innerText = "X";
    deleteButton.addEventListener("click", async () => {
        try {
            const response = await axios.delete(`/api/cupcakes/${cupcake.id}`);
            if (response.status === 200) {
                newCupcake.remove();
            }
        } catch (error) {
            if (error.response && error.response.status === 404) {
                // If the cupcake doesn't exist in the backend, just remove it from the frontend
                newCupcake.remove();
            } else {
                console.error("An error occurred while deleting the cupcake");
            }
        }
    });

    cupcakeDetails.append(deleteButton);
    newCupcake.append(cupcakeDetails);

    if (cupcake.image) {
        const cupcakeImage = document.createElement("img");
        cupcakeImage.src = cupcake.image;
        cupcakeImage.alt = `${cupcake.flavor} cupcake`;
        cupcakeImage.style.width = '100px';
        cupcakeImage.style.height = '100px';
        newCupcake.append(cupcakeImage);
    }

    cupcakeList.append(newCupcake);

}

async function getAllCupcakes() {
    const response = await axios.get("/api/cupcakes");
    const cupcakes = response.data.cupcakes; //list of cupcake objects

    for (let cupcake of cupcakes) {
        appendCupcake(cupcake);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("new-cupcake-form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const flavor = document.getElementById("flavor").value;
        const size = document.getElementById("size").value;
        const rating = parseFloat(document.getElementById("rating").value);
        const image = document.getElementById("image").value || null;
    
        const cupcakeData = {
            flavor,
            size,
            rating,
            image
        };
    
        try {
            const response = await axios.post("/api/cupcakes", cupcakeData);
            if (response.status === 201) {
                appendCupcake(response.data.cupcake);
            } else {
                console.error("error");
            }
        } catch (error) {
            console.error("An error occurred while submitting the form:");
        }
    });

    getAllCupcakes();
});