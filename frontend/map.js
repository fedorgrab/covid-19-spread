let map;
let numberOfPolygonsToProcess;
let numberOfProcessedPolygons = 0;

function getStyleProvincePolygon(province) {
  let colorCoeff = province.getProperty("color");
  
  if (numberOfPolygonsToProcess - numberOfProcessedPolygons <= 25) {
    let scrollToPixel = document.getElementById("header-stat").offsetHeight;
    window.scrollTo({top: scrollToPixel, behavior: 'smooth'});
  }
  // Additional scaling
  colorCoeff = colorCoeff < 0.05 ? colorCoeff * 2. : colorCoeff;
  colorCoeff = 0.5 <= colorCoeff < 0.1 ? colorCoeff * 1.7 : colorCoeff;
  numberOfProcessedPolygons += 1;
  return ({
    fillColor: "#f65c5d",
    strokeColor: "black",
    fillOpacity: colorCoeff * 0.8,
    strokeOpacity: 1.,
    strokeWeight: 0.45
  });
}

function getStyleProvincePolygon2(province) {
  let colorCoeff = province.getProperty("color");
  // Additional scaling
  colorCoeff = colorCoeff < 0.05 ? colorCoeff * 2. : colorCoeff;
  colorCoeff = 0.5 <= colorCoeff < 0.1 ? colorCoeff * 1.7 : colorCoeff;
  
  return ({
    fillColor: "red",
    strokeColor: "black",
    fillOpacity: 0.9,
    strokeOpacity: 1.,
    strokeWeight: 0.45
  });
}

function getMapProperties() {
  return {
    center: new google.maps.LatLng(MAP_CENTER.LAT, MAP_CENTER.LONG),
    zoom: 1.5,
    mapTypeControlOptions: {mapTypeIds: MAP_TYPE_IDS},
    disableDefaultUI: true,
    restriction: {latLngBounds: MAP_RESTRICTION_BOUNDS, strictBounds: false}
  }
}

function setMapStyle(mapStyle) {
  let name = "Coronavirus Spread Heat Map";
  const styledMapType = new google.maps.StyledMapType(
    mapStyle, {name: name}
  );
  map.mapTypes.set("styled_map", styledMapType);
  map.setMapTypeId("styled_map");
}


function setWorldStats(worldStats) {
  document.getElementById("world-total-confirmed").innerHTML = worldStats["casesConfirmed"];
  document.getElementById("world-total-deaths").innerHTML = worldStats["casesDeaths"];
  document.getElementById("world-total-recovered").innerHTML = worldStats["casesRecovered"];
  
  document.getElementById("world-today-confirmed").innerHTML = worldStats["casesConfirmedNew"];
  document.getElementById("world-today-deaths").innerHTML = worldStats["casesDeathsNew"];
  document.getElementById("world-today-recovered").innerHTML = worldStats["casesRecoveredNew"];
}

async function initMap() {
  map = new google.maps.Map(
    document.getElementById("googleMap"), getMapProperties()
  );
  setMapStyle(MAP_STYLE_BLACK);
  
  let worldStats = await backend.getDailyUpdateRequest();
  setWorldStats(worldStats);
  
  let geojson = await backend.getGeoSpreadRequest();
  numberOfPolygonsToProcess = geojson.features.length;
  
  map.data.addGeoJson(geojson);
  map.data.setStyle(getStyleProvincePolygon);
  
  map.data.addListener('click', function (event) {
    textContent = includeTextContent(event.feature);
    document.getElementById('info-box').innerHTML = textContent;
  });
  
  map.data.addListener('mouseover', function (event) {
    map.data.revertStyle();
    map.data.overrideStyle(event.feature, {strokeWeight: 2});
  });
  
  map.data.addListener('mouseout', function (event) {
    map.data.revertStyle();
  });
}

