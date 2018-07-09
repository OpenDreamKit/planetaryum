async function fetch_meta() {
    return await (await fetch('meta.json')).json();
}

function init_components() {
    Vue.component('thumb', {
	props: ['nb'],
	template: '<div>{{ nb.name }}</div>',
    });
}


(async function() {
    try {
	let db = await fetch_meta();

	init_components();
	
	let app = new Vue({
	    el: '#planetaryum',
	    data: {
		db: db,
	    }
	})
    } catch (e) {
	console.error(e);
    }
})();
