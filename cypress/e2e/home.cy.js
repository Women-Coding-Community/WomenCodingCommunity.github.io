describe('Home page', () => {
  it('should exist', () => {
    cy.visit('https://womencodingcommunity.com/')

    cy.request('https://womencodingcommunity.com/')
      .its('status')
      .should('eq', 200)
  })
})