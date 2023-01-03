mapboxgl.accessToken = 'pk.eyJ1IjoiYXNtaTY2IiwiYSI6ImNsYzUzdG4zazNucHQzdXBuaGVpbDY4bmkifQ.DaZdS1kpQHCtJJhP_b_BTg';
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [-99.1331785, 19.4326296], // starting position
    zoom: 10.5,
    _language: "es"
});
mapboxgl.setRTLTextPlugin('https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.2.3/mapbox-gl-rtl-text.js');
map.addControl(new MapboxLanguage({
    defaultLanguage: 'es'
}));
// getRoute(end);
// create a function to make a directions request
async function getRoute(inicio, fin) {
    // make a directions request using cycling profile
    // an arbitrary start will always be the same
    // only the end or destination will change
    const query = await fetch(
        `https://api.mapbox.com/directions/v5/mapbox/driving/${inicio[0]},${inicio[1]};${fin[0]},${fin[1]}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`,
        { method: 'GET' }
    );
    const json = await query.json();
    const data = json.routes[0];
    const route = data.geometry.coordinates;
    const geojson = {
        type: 'Feature',
        properties: {},
        geometry: {
            type: 'LineString',
            coordinates: route
        }
    };
    
    // if the route already exists on the map, we'll reset it using setData
    if (map.getSource('route')) {
        map.getSource('route').setData(geojson);
        map.getSource('point').setData({
                    type: 'FeatureCollection',
                    features: [
                        {
                            type: 'Feature',
                            properties: {},
                            geometry: {
                                type: 'Point',
                                coordinates: inicio
                            }
                        }
                    ]
                });
        map.getSource('point2').setData({
                    type: 'FeatureCollection',
                    features: [
                        {
                            type: 'Feature',
                            properties: {},
                            geometry: {
                                type: 'Point',
                                coordinates: fin
                            }
                        }
                    ]
                });
        
    }
    // otherwise, we'll make a new request
    else {
        
        map.loadImage("../../static/img/iconos/posicion.png", (error, image) => {
            if (error) throw error;
            map.addImage('store-icon', image, { 'sdf': true });
            // map.addSource('food-stores', {
            //     'type': 'vector',
            //     'url': 'mapbox://examples.dl46ljcs'
            // });
        });

        // Add starting point to the map
        map.addLayer({
            id: 'point',
            type: 'symbol',
            source: {
                type: 'geojson',
                data: {
                    type: 'FeatureCollection',
                    features: [
                        {
                            type: 'Feature',
                            properties: {},
                            geometry: {
                                type: 'Point',
                                coordinates: inicio
                            }
                        }
                    ]
                }
            },
            'layout': {
                'icon-image': 'store-icon',
                'icon-size': 0.25
            },
            'paint': {
                'icon-color': '#ff5733'
            }
        });
        
        // this is where the code from the next step will go
        map.addLayer({
            id: 'point2',
            type: 'symbol',
            source: {
                type: 'geojson',
                data: {
                    type: 'FeatureCollection',
                    features: [
                        {
                            type: 'Feature',
                            properties: {},
                            geometry: {
                                type: 'Point',
                                coordinates: fin
                            }
                        }
                    ]
                }
            },
            'layout': {
                'icon-image': 'store-icon',
                'icon-size': 0.25
            },
            'paint': {
                'icon-color': '#ff5733'
            }
        });
        map.addLayer({
            id: 'route',
            type: 'line',
            source: {
                type: 'geojson',
                data: geojson
            },
            layout: {
                'line-join': 'round',
                'line-cap': 'round'
            },
            paint: {
                'line-color': '#ff5733',
                'line-width': 5,
                'line-opacity': 0.75
            }
        });
        
    }
    map.fitBounds([inicio, fin], {
            padding: 50
        });
}


map.on('click', 'places', (e) => {
    // Copy coordinates array.
    const coordinates = e.features[0].geometry.coordinates.slice();
    const description = e.features[0].properties.description;

    // Ensure that if the map is zoomed out such that multiple
    // copies of the feature are visible, the popup appears
    // over the copy being pointed to.
    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
    }

    new mapboxgl.Popup()
        .setLngLat(coordinates)
        .setHTML(description)
        .addTo(map);
});

// Change the cursor to a pointer when the mouse is over the places layer.
map.on('mouseenter', 'places', () => {
    // console.log("entre")
    map.getCanvas().style.cursor = 'pointer';
});

// Change it back to a pointer when it leaves.
map.on('mouseleave', 'places', () => {
    map.getCanvas().style.cursor = '';
});
map.on('load', () => {
        // make an initial directions request that
        // starts and ends at the same location
        map.addSource('places', {
            'type': 'geojson',
	            'data': {
		                'type': 'FeatureCollection',
			                'features': [
                    {
                    'type': 'Feature',
                    'properties': {
                        'description':
                            '<strong>Lindavista</strong><p>Av. Juan de Dios Bátiz 523, Zacatenco, Gustavo A. Madero, 07340 Ciudad de México, CDMX</p>',
                        'icon': 'post'
                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-99.13241777989998, 19.503812618644453]
                    }
                }
                ,
							
                    {
                    'type': 'Feature',
                    'properties': {
                        'description':
                            '<strong>Sátelite</strong><p>Cto. Cirujanos 1-Local 3, Cd. Satélite, 53100 Naucalpan de Juárez, Méx.</p>',
                        'icon': 'post'
                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-99.23202789711353, 19.510418491079623]
                    }
                }
                ,
							
                    {
                    'type': 'Feature',
                    'properties': {
                        'description':
                            '<strong>Colonia del Valle</strong><p>C. Gabriel Mancera 916, Col del Valle Centro, Benito Juárez, 03100 Ciudad de México, CDMX</p>',
                        'icon': 'post'
                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-99.16479674838662, 19.38370135021779]
                    }
                }
                ,
							
                    {
                    'type': 'Feature',
                    'properties': {
                        'description':
                            '<strong>Villa de Aragón</strong><p>Av.608, 4a Sección, San Juan de Aragón, Gustavo A. Madero, 07979 Ciudad de México, CDMX</p>',
                        'icon': 'post'
                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-99.0612996325149, 19.46156136421477]
                    }
                }
                ,
							
                    {
                    'type': 'Feature',
                    'properties': {
                        'description':
                            '<strong>Polanco</strong><p>Av. Ejército Nacional Mexicano 598, Polanco, CDMX</p>',
                        'icon': 'post'
                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-99.1949207882933, 19.43566665558206]
                    }
                }
                ,
							                            ]
			                        }
		                    });
	                    map.addLayer({
	                        'id': 'places',
		                        'type': 'symbol',
		                        'source': 'places',
		                        'layout': {
		                            'icon-image': ['get', 'icon'],
			                            'icon-size': 0.5,
			                            'icon-allow-overlap': true
			                        }
		                    });
                });
        
let coordinatesPoints = new Map();
                
coordinatesPoints.set('Lindavista',[-99.13241777989998, 19.503812618644453])
            
                
coordinatesPoints.set('Sátelite',[-99.23202789711353, 19.510418491079623])
            
                
coordinatesPoints.set('Colonia del Valle',[-99.16479674838662, 19.38370135021779])
            
                
coordinatesPoints.set('Villa de Aragón',[-99.0612996325149, 19.46156136421477])
            
                
coordinatesPoints.set('Polanco',[-99.1949207882933, 19.43566665558206])
            
function convertMyRoute(inicio, fin){
                    getRoute(coordinatesPoints.get(inicio), coordinatesPoints.get(fin))
                }