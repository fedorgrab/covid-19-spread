function getValueOrDash(feature, property) {
  let value = feature.getProperty(property);
  return value ? value : "-"
}

function includeTextContent(feature) {
  const countryName = feature.getProperty("country");
  const provinceName = feature.getProperty("province");
  
  const casesConfirmed = getValueOrDash(feature, "cases_confirmed");
  const casesDeaths = getValueOrDash(feature, "cases_deaths");
  const casesRecovered = getValueOrDash(feature, "cases_recovered");
  
  const provinceBlock = provinceName === "not_given" ? `` : `, ${provinceName}`;
  const locationText = `${countryName}${provinceBlock}`;
  const styleClassSuffix = siteColorTheme === "white" ? "-white-theme" : "";
  return `
<div>
<span class="location-label">${locationText}</span>
  <div class="stat-container">
    <div class="stat-value">
      <span >${casesConfirmed}</span><br>
      <span class="color-red${styleClassSuffix}">${casesDeaths}</span><br>
      <span class="color-green${styleClassSuffix}">${casesRecovered}</span>
    </div>
    <div class="stat-label color-gray-small${styleClassSuffix}">
      <span>Confirmed</span><br>
      <span>Deaths</span><br>
      <span>Recovered</span>
    </div>
  </div>
</div>
`
}
