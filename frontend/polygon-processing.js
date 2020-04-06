// Greater than number of countries in the world, because the website shows provinces.
let numberOfPolygonsToProcess = 275;
let numberOfProcessedPolygons = 0;
let polygonsProcessed = false;
let scrollPolygonCounter = 0;

function trackScroll() {
  let scrollToPixel = document.getElementById("header-stat").offsetHeight;
  if (numberOfPolygonsToProcess <= numberOfProcessedPolygons) {
    if (!polygonsProcessed) {
      window.scrollTo({top: scrollToPixel, behavior: "smooth"});
      polygonsProcessed = true;
    }
    if (document.documentElement.scrollTop !== scrollToPixel) {
      scrollPolygonCounter += 1;
      if (scrollPolygonCounter % 40 === 0) {
        window.scrollTo({top: scrollToPixel, behavior: "smooth"});
      }
    }
  }
}

function getStyleProvincePolygon(province) {
  trackScroll();
  let colorCoeff = province.getProperty("color");
  // Additional scaling
  colorCoeff = colorCoeff < 0.05 ? colorCoeff * 2. : colorCoeff;
  numberOfProcessedPolygons += 1;
  return ({
    fillColor: "#f65c5d",
    strokeColor: "black",
    fillOpacity: colorCoeff * 0.8,
    strokeOpacity: 1.,
    strokeWeight: 0.45
  });
}
