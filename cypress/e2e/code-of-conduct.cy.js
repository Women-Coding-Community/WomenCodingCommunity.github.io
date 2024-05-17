describe('Tests Mentorship Code of Conduct page', () => {
    const SLACK_LINK = "https://join.slack.com/t/womencodingcommunity/shared_invite/zt-2hpjwpx7l-rgceYBIWp6pCiwc0hVsX8A";

    beforeEach(() => {
        cy.visit(`${Cypress.config().baseUrl}/mentorship-code-of-conduct`);
    });

    describe('Verify UI elements from Header and Main content', () => {
        it('should verify UI elements on the Code of Conduct page', () => {
            cy.contains('Show More').should('be.visible');
            cy.contains('Read').should('be.visible');
        });

        it('should find Slack link within #mentee-section and verify URL and text', () => {
            cy.get('#mentee-section')
                .find("a[href='" + SLACK_LINK + "']")
                .should('exist')
                .contains('Slack')
        })
    })

    describe('Test "Show more," "Show less," for mentee and mentor', () => {

        it('should verify the existence of the anchor tag with mentee bottom learn more and Show More text', () => {
            cy.get('a#btn-mentee-learn-more').should('be.visible').contains('Show More').should('be.visible');
            cy.get('a#btn-mentee-learn-more').click();
            cy.get('a#btn-mentee-show-less:contains("Show Less")', { defaultCommandTimeout: 1000 }).should('be.visible');
        });

        it('should verify the existence of the anchor tag with mentor bottom learn more and Show More text', () => {
            cy.get('a#btn-mentor-learn-more').should('be.visible').contains('Show More').should('be.visible');
            cy.get('a#btn-mentor-learn-more').click();
            cy.get('a#btn-mentee-show-less:contains("Show Less")', { timeout: 10000 }).should('exist');
        });

    })

    describe('Test navigation to the community Code of Conduct page', () => {
        it('should redirect from mentorship code of conduct to the community code of conduct', () => {
            cy.contains('Read').click();
            cy.url().should('eq', `${Cypress.config().baseUrl}/code-of-conduct`);
        });
    })

    describe('Verify all footer UI elements', () => {

        it('should verify the visibility of footer UI elements', () => {
            cy.get('.brand').should('be.visible');
            cy.contains("Women Coding Community is a not-for-profit organisation.").should('be.visible');
            cy.contains('Follow Us').should('be.visible');
            cy.contains('Join us on social media and stay tuned.').should('be.visible');
            cy.contains('© 2024 Women Coding Community').should('be.visible');
        });

        it('should verify LinkedIn link', () => {
            cy.get('.network a[href="https://www.linkedin.com/company/womencodingcommunity"]')
                .should('be.visible')
                .should('exist')
                .should('have.attr', 'target', '_blank')
        });

        it('should verify Slack link', () => {
            cy.get(".network a[href='"+SLACK_LINK+"']")
                .should('exist')
                .should('have.attr', 'target', '_blank')
                .should('have.attr', 'href', SLACK_LINK);
        });

        it('should verify GitHub link', () => {
            cy.get('.network a[href="https://github.com/WomenCodingCommunity"]')
                .should('be.visible')
                .should('exist')
                .should('have.attr', 'target', '_blank')
        });

        it('should verify Instagram link', () => {
            cy.get('.network a[href="https://www.instagram.com/women_coding_community"]')
                .should('be.visible')
                .should('exist')
                .should('have.attr', 'target', '_blank')
        });

        it('should verify Email link', () => {
            cy.get('.network a[href="mailto:london@womencodingcommunity.com"]')
                .should('be.visible')
                .should('exist')
                .should('have.attr', 'target', '_blank')
        });

        it('should verify Twitter link', () => {
            cy.get('.network a[href="https://twitter.com/WCC_Community"]')
                .should('be.visible')
                .should('exist')
                .should('have.attr', 'target', '_blank')
        });
    });
});
