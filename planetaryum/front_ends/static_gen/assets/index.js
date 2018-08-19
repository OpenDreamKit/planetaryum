/* Fetch the metadata on notebooks */
async function fetch_meta() {
    return await (await fetch('meta.json')).json();
}

/* Vue JS App */
(async function() {
    let db_promise = fetch_meta();

    /************* Components ***************/
    /* The notebook thumbnail gallery */
    Vue.component('plyum-gallery', {
	data() {
	    return { expanded: !this.isThereANB() };
	},
	props: ['nbs'],
	template: `<div id="gallery" :class="expanded ? 'expanded' : 'contracted'">
  <plyum-thumb
    v-for="i in nbs"
    v-bind:nb="i"
    v-bind:key="i._id">
  </plyum-thumb>
</div>`,
	watch: {
	    // Update class when browsing occurs
	    '$route': function() {
		this.expanded = !this.isThereANB();
	    }
	},
	methods: {
	    // Test if a notebook is open in the router view
	    isThereANB() {
		return this.$router.getMatchedComponents().length > 0;
	    }
	},
	components: {
	    /* The individual thumbnails (glorified links) */
	    'plyum-thumb': {
		props: ['nb'],
		template: `<div class="thumb">
  <router-link v-bind:to="'/nb/' + nb._id">
    <div class="figure"><img v-bind:src="getThumb()"></div>
    <div class="caption">{{ nb.name }}</div>
  </router-link>
</div>`,
		methods: {
		    getThumb() {
			if (this.$props.nb.meta.thumbs.length) {
			    return this.$props.nb.meta.thumbs[0];
			} else {
			    return 'assets/thumbs/jupyter.svg';
			}
		    },
		},
	    }
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

    /************* Register app ***************/
    try {
	// Wait for metadata
	const data = await db_promise;
	// Init app
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
	})
    } catch (e) {
	console.error(e);
    }
})();
