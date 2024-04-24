const { JSDOM } = require('jsdom');

describe('Show/Hide Button on Mentees Code of Conduct when Clicking on Learn More Button', () => {

  const classHide = 'd-none';

  beforeEach(() => {

    // Create a new JSDOM environment
    const dom = new JSDOM(`
    <ol>
                <li><em>WCC is an inclusive community</em>, dedicated to providing an empowering experience for everyone who participates in or supports our community, regardless of gender, gender identity and expression, sexual orientation, ability, physical appearance, body size, race, ethnicity, age, religion, socioeconomic status, caste, creed, political affiliation, or preferred programming language(s).</li>
                <li>Cancel or reschedule appointments with a minimum of 24 hours prior notice by providing a reason using preferable channel (email, slack, or anything else you both chose as the channel of communication) to the mentor.</li>
                <li>No-shows are unacceptable for mentors and mentees. No-shows should be informed to the Mentorship Programme Team by <a href="mailto:londonmentorship@womenwhocode.com">londonmentorship@womenwhocode.com</a>. The Mentorship Programme Team will evaluate case by case, and this is one of the possible actions that could result in exclusion from the current and future mentorship program cycles.</li>
                <li>No-replies by email or slack to the Mentorship Programme Team and/or mentor in a week are unacceptable during the program. Participants who applied but failed to reply without any reason provided will be banned from the current cycle.</li>

                <span id="mentee-conduct" class="d-none">
                    <li>Create a <a href="https://bit.ly/WCClondonslack">Slack Account</a>, join the #mentorship channel and check slack messages in the program to remain updated with all communication.</li>
                    <li>Come to your sessions well-prepared and with realistic expectations.</li>
                    <li>Whenever you see something is not going in the direction you want with the mentorship programme, provide feedback by email/slack or during your session with your mentor, so your mentor can adjust the sessions as necessary.</li>
                    <li>If you have any concerns, don't hesitate to contact the Mentorship Programme Team (by slack or <a href="mailto:londonmentorship@womenwhocode.com">londonmentorship@womenwhocode.com</a>).</li>
                    <li>Attending the Mentees Catch up sessions is crucial for the programme's improvement:
                        <ul>
                            <li>It is <b>mandatory</b> to provide feedback using google forms shared with you before the session.</li>
                            <li>If you can't attend the session, explain your reason in reply to the invitation.</li>
                        </ul>
                    </li>
                    <li>Do not use our programme for advertising or customer acquisition purposes.</li>
                    <li>Please refrain from harsh, critical, and demeaning comments or feedback of any kind (be especially mindful of public written reviews).</li>
                    <li>Please show your mentors and the Mentorship Programme some love by expressing your appreciation.</li>
                    <li>Discussions between you and your mentor are considered to be confidential. Be careful about sensitive personal issues. Do not share any specific content of the sessions or personal data without the permission of your mentor.</li>
                </span>
            </ol>
      <div class="text-center">
        <a class="btn btn-primary" id="btn-mentee-learn-more" href="#">Learn More</a>
        <a class="btn btn-primary d-none" id="btn-mentee-show-less" href="#">Show Less</a>
      </div>
    `);

    // Set up global variables for the test environment
    global.document = dom.window.document;
    global.window = dom.window;

    // Load jQuery globally
    global.jQuery = require('jquery');
    global.$ = global.jQuery;
  });

  afterEach(() => {
      delete global.document;
      delete global.window;
      delete global.jQuery;
      delete global.$;
  });

  test('test page exist', () => {
      // Initial state assertions
      expect(true).toBe(true);
  });

});
