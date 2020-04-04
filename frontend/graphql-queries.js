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
