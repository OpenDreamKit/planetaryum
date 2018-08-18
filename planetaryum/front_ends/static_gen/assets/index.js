async function fetch_meta() {
    return await (await fetch('meta.json')).json();
}

(async function() {
    let db_promise = fetch_meta();
    
    Vue.component('plyum-thumb', {
	props: ['nb'],
	template: `<div class="thumb">
  <router-link v-bind:to="'/nb/' + nb._id">
    <img v-bind:src="getThumb()">
    <span>{{ nb.name }}</span>
  </router-link>
</div>`,
	methods: {
	    getThumb() {
		// TODO: improve this
		if (this.$props.nb.meta.thumbs.length) {
		    return this.$props.nb.meta.thumbs[0];
		} else {
		    return '';
		}
	    },
	},
    });

    const Notebook = {
	data() {
	    return {
		loading: false,
		html: null,
	    };
	},
	created() {
	    this.fetchNB();
	},
	watch: {
	    '$route': 'fetchNB'
	},
	props: ['nb'],
	template: `<div v-html="html"></div>`,
	methods: {
	    fetchNB() {
	    	fetch(this.$props.nb.path)
		    .then(res => res.text())
		    .then(html => this.html = html);
	    },
	},
    };

    try {
	const data = await db_promise;
	let app = new Vue({
	    el: '#planetaryum',
	    data: {
		db: data,
	    },
	    router: new VueRouter({
		routes: data.map((nb) => ({
		    path: `/nb/${nb._id}`,
		    component: Notebook,
		    props: { nb },
		})),
	    }),
	    methods: {
	    },
	})
    } catch (e) {
	console.error(e);
    }
})();
