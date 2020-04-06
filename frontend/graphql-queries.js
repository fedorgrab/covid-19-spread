const dailyUpdateRecordQuery = `
{
  dailyUpdateRecords(last: 1) {
    edges {
      node {
        casesConfirmed
        casesDeaths
        casesRecovered
        casesConfirmedNew
        casesDeathsNew
        casesRecoveredNew
      }
    }
  }
}`;


function dayOneCountryQuery(country) {
  return `
  {
    dayOneRecords(country: "${country}") {
      edges {
        node {
          country
          casesConfirmed
          casesDeaths
          casesRecovered
          date
        }
      }
    }
  }`;
}
