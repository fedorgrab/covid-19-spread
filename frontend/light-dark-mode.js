let siteColorTheme = "black";

function setInfoBlockStyle(styleType) {
  let infoBlockBackground = styleType === "white" ? "#ededed" : "#192331";
  let infoBlockColor = styleType === "white" ? "black" : "white";
  
  let infoBlock = document.getElementById("info-box");
  infoBlock.style.backgroundColor = infoBlockBackground;
  infoBlock.style.color = infoBlockColor;
}

function changeStyleOnElementsWithClass(fromClass, toClass) {
  Array.from(document.getElementsByClassName(fromClass)).map((el) => {
    el.classList.add(toClass);
    el.classList.remove(fromClass);
  });
}

function setHeaderFooterStyle(styleType) {
  for (let i = 0; i < INVERTING_STYLE_CLASSES.length; i++) {
    let fromClass = styleType === "white" ? INVERTING_STYLE_CLASSES[i] : `${INVERTING_STYLE_CLASSES[i]}-white-theme`;
    let toClass = styleType === "white" ? `${INVERTING_STYLE_CLASSES[i]}-white-theme` : INVERTING_STYLE_CLASSES[i];
    changeStyleOnElementsWithClass(fromClass, toClass);
  }
}

function toggleSwitch() {
  let checkbox = document.getElementById("customSwitch1");
  let checked = checkbox.checked;
  let mapStyle = checked ? MAP_STYLE_WHITE : MAP_STYLE_BLACK;
  siteColorTheme = checked ? "white" : "black";
  
  setMapStyle(mapStyle);
  setInfoBlockStyle(siteColorTheme);
  setHeaderFooterStyle(siteColorTheme);
}
