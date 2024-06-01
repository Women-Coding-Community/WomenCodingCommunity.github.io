describe('Tests Mentorship Code of Conduct page', () => {
    const SLACK_LINK = "https://join.slack.com/t/womencodingcommunity/shared_invite/zt-2hpjwpx7l-rgceYBIWp6pCiwc0hVsX8A";
    const BE_VISIBLE = 'be.visible';
    beforeEach(() => {
        cy.visit(`${Cypress.config().baseUrl}/mentorship-code-of-conduct`);
    });

    describe('Verify UI elements from Header and Main content', () => {
        it('should verify UI elements on the Code of Conduct page', () => {
            const IGNORE_CASE = {matchCase: false};
            
            cy.contains("Mentorship Code of Conduct", IGNORE_CASE).should(BE_VISIBLE);
            cy.contains("Code Of Conduct for Mentees", IGNORE_CASE).should(BE_VISIBLE);
            cy.contains("Code Of Conduct for Mentors", IGNORE_CASE).should(BE_VISIBLE);
            cy.contains('Show More').should(BE_VISIBLE);
            cy.contains('Read').should(BE_VISIBLE);
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
            cy.get('a#btn-mentee-learn-more').should(BE_VISIBLE).contains('Show More').should(BE_VISIBLE);
            cy.get('a#btn-mentee-learn-more').click();
            cy.get('a#btn-mentee-show-less:contains("Show Less")', { defaultCommandTimeout: 1000 }).should(BE_VISIBLE);
        });

        it('should verify the existence of the anchor tag with mentor bottom learn more and Show More text', () => {
            cy.get('a#btn-mentor-learn-more').should(BE_VISIBLE).contains('Show More').should(BE_VISIBLE);
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
            cy.get('.brand').should(BE_VISIBLE);
            cy.contains("Women Coding Community is a not-for-profit organisation.").should(BE_VISIBLE);
            cy.contains('Follow Us').should(BE_VISIBLE);
            cy.contains('Join us on social media and stay tuned.').should(BE_VISIBLE);
            cy.contains('© 2024 Women Coding Community').should(BE_VISIBLE);
        });

        it('should verify LinkedIn link', () => {
            cy.get('.network a[href="https://www.linkedin.com/company/womencodingcommunity"]')
                .should(BE_VISIBLE)
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
                .should(BE_VISIBLE)
                .should('exist')
                .should('have.attr', 'target', '_blank')
        });

        it('should verify Instagram link', () => {
            cy.get('.network a[href="https://www.instagram.com/women_coding_community"]')
                .should(BE_VISIBLE)
                .should('exist')
                .should('have.attr', 'target', '_blank')
        });

        it('should verify Email link', () => {
            cy.get('.network a[href="mailto:london@womencodingcommunity.com"]')
                .should(BE_VISIBLE)
                .should('exist')
                .should('have.attr', 'target', '_blank')
        });

        it('should verify Twitter link', () => {
            cy.get('.network a[href="https://twitter.com/WCC_Community"]')
                .should(BE_VISIBLE)
                .should('exist')
                .should('have.attr', 'target', '_blank')
        });
    });
});
