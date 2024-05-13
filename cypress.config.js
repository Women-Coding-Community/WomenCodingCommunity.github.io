const { defineConfig } = require("cypress");

module.exports = defineConfig({
  defaultCommandTimeout: 2000,
  e2e: {    
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
    baseUrl: 'https://womencodingcommunity.com',
  },
});
