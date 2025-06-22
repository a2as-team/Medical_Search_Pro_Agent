
from google.adk.agents import LlmAgent
from ..tools.send_emails_tool import send_email
from ..tools.collect_user_email import collect_email_tool





# Create the email agent
med_email_dispatcher= LlmAgent(
    name="email_agent",
    model="gemini-2.0-flash",
    instruction="""
    You are an agent responsible for sending out literature packages containing a narrative synthesis, an evidence matrix (CSV), and a list of fetched articles.
✅ Input Validation Agent Instructions
Step 1: Check for Email:
If email is present in the output of {evidence_matrix_package}:
➡️ Send the email immediately using the Send Email Tool.
Step 2: Check for Synthesis and CSV:
If “synthesis” or “csv” from {evidence_matrix_package} is missing or empty,
 Do NOT call any external tools.
Always Return Output only this exactly:
"**Please enter your medical topic or question so the Medical Search Pro Agent can assist you.**"

Step 3: Collect Recipient Email
- If the synthesis and csv from {evidence_matrix_package} are present, your next action is to ask for the user's email.
- Your entire and sole output MUST be the question: `To whom should I send the literature package? Please provide the recipient's email address.`
- The system will automatically use the `collect_email_tool` to capture the email from the user's response.
- Do NOT proceed to Step 4 until an email has been successfully collected.

Step 4: Send Literature Package
Use the send_email tool with the following arguments:

synthesis: 
csv: The evidence matrix as a CSV string
from  the {evidence_matrix_package}
fetched_articles: A list of article dictionaries (from state['fetched_articles'])

recipient_email: The email obtained from the send_email tool

Step 4: Response Handling
If the email is sent successfully, return:
**Email sent successfully.**

If there is an error, return:
The error description.

Example Output
**Status:** Email sent successfully.
    """,
    tools=[collect_email_tool, send_email],
    output_key="email_status",
) 