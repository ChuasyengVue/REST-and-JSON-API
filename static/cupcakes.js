BASE_URL = "http://127.0.0.1:5000/api"


// Put cupcake on page
async function showCupcakes(){
    resp = await axios.get(`${BASE_URL}/cupcakes`);

    for(let cupcakeData of resp.data.cupcakes){
        let newCupcake = $(cupcakeData);
        $("#cupcake-list").append(newCupcake);
    }
}


// Add a new cupcake
$('#create-new-cupcake').on("submit", async function(evt){
evt.preventDefault();

let flavor = $("#form-flavor").val();
let rating = $("#form-rating").val();
let size = $("#form-size").val();
let image = $("#form-image").val();

const newCupcakeResp = await axios.post(`${BASE_URL}/cupcakes`,{
    flavor,
    rating,
    size,
    image
});

let newCupcake = $(newCupcakeResp.data.cupcake)
$("#cupcake-list").append(newCupcake);
$("#create-new-cupcake").trigger("reset");
});


// Delete a cupcake
$('.delete-cupcake').click(deleteCupcake)

async function deleteCupcake(){
    const id = $(this).data('id')
    await axios.delete(`/api/cupcakes/${id}`)
    $(this).parent().remove()
}


$(showCupcakes);