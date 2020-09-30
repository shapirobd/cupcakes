const BASE_URL = "http://127.0.0.1:5000/api";

async function showInitialCupcakes() {
	const resp = await axios.get(`${BASE_URL}/cupcakes`);

	for (let cupcake of resp.data.cupcakes) {
		let newCupcake = $(generateCupcakeHTML(cupcake));
		$("#cupcakes-list").append(newCupcake);
	}
}

$("#create-cupcake-form").on("submit", async function (evt) {
	evt.preventDefault();
	let flavor = $("#form-flavor").val();
	let size = $("#form-size").val();
	let rating = $("#form-rating").val();
	let image = $("#form-image").val();

	const resp = await axios.post(`${BASE_URL}/cupcakes`, {
		flavor,
		size,
		rating,
		image,
	});

	let newCupcake = $(generateCupcakeHTML(resp.data.cupcake));

	$("#cupcakes-list").append(newCupcake);
	$("#create-cupcake-form").trigger("reset");
});

function generateCupcakeHTML(cupcake) {
	return `<div class="col col-4">
		<img
			class="img img-fluid img-thumbnail my-3"
			src="${cupcake.image}"
			alt=""/>
		<h4>Flavor: ${cupcake.flavor}</h4>
		<h4>Size: ${cupcake.size}</h4>
		<h4>Rating: ${cupcake.rating}</h4>
	</div>`;
}

$(showInitialCupcakes());
