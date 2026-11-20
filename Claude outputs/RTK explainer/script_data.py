# Single source for the "Right-to-Know Request Portal" explainer.
# Edit narration or pictures here, then run _source/make_cards.py (if a card changed),
# _source/make_docs.py and build_video.py.
#
# Segment kinds
#   hold : a still with no narration, held for `secs`
#   narr : one paragraph of narration, read by ElevenLabs; `pics` share its length
#
# A picture is "file" or "file|push" (slow push-in). Paths are relative to this folder.
# cards/ are drawn by _source/make_cards.py. portal_shots/ are real screens of the RTK Portal
# running on invented test data, captured by _source/capture_portal.py.

TITLE = "A Right-to-Know Request Portal for the Claremont School District"
NAME = "RTK-Portal-explainer"
SIZE = (1920, 1080)
FPS = 30
PARTS = {1: "What the portal is", 2: "How a request moves", 3: "Why Anthropic"}

def N(sid, text, *pics):
    return dict(id=sid, kind="narr", part=int(sid.split(".")[0]), text=text, pics=list(pics))

SEGMENTS = [
    dict(id="T0", kind="hold", secs=4.0, pics=["cards/title.png"]),

    # ---------------------------------------------------------------- Part 1
    N("1.01", "This is a short introduction to a Right-to-Know request portal, built for the Claremont School District. "
              "It shows how a request would move through the portal. It also explains why the project is asking a "
              "company called Anthropic for support.",
      "cards/title.png", "portal_shots/13_home_after.jpg|push"),
    N("1.02", "New Hampshire's Right-to-Know Law, R-S-A ninety-one A, gives every citizen the right to inspect public "
              "records. When a record is not immediately available, the District has five business days to produce it, "
              "deny the request in writing, or say in writing when it will answer.",
      "cards/law.png"),
    N("1.03", "In September of twenty twenty-five, the School Board adopted Policy E-H. It directs the Superintendent's "
              "procedures to include, in the policy's words, a method for logging and tracking both the requests and "
              "the responses. The policy also allows that log to be posted on the District's website.",
      "cards/policy.png|push"),
    N("1.04", "The portal is one way to do that. A resident files a request online. The portal logs it, puts it in "
              "line, and prepares a draft response. District staff review and send every response. Then the request "
              "and the response appear on a public log.",
      "cards/overview.png"),

    # ---------------------------------------------------------------- Part 2
    N("2.01", "Here is how a request moves. The screens you are about to see are the working portal, running on "
              "invented test requests. A resident describes the records they want, and confirms an email address with "
              "a six-digit code. The request then gets a public number, and a due date on the fifth business day.",
      "portal_shots/02_form_top.jpg", "portal_shots/03_verify_code.jpg", "portal_shots/04_filed_status.jpg"),
    N("2.02", "Requests are handled one at a time, in a fair order. A person's first open request goes ahead of "
              "anyone's second. So one person who files many requests does not hold up everyone else.",
      "cards/queue.png"),
    N("2.03", "Next, the portal sorts the request into one of five outcomes, and writes a draft to match. The most "
              "common is expected to be a records search, for a record that is not posted anywhere. Other drafts point "
              "to a record that is already public, offer combined figures about students, or cite the exemption that "
              "applies.",
      "cards/outcomes.png"),
    N("2.04", "The first sorting is done by fixed rules. When it is switched on, Claude, an A-I model made by "
              "Anthropic, can then search the public record and prepare the draft. Either way, the portal accepts "
              "legal citations only from an approved list.",
      "cards/triage.png", "portal_shots/05_console_top.jpg|push"),
    N("2.05", "Nothing is sent automatically. A staff member at the Superintendent's office reads the draft, edits "
              "it, and sends it. If a draft still has a blank to fill in, the portal refuses to send it.",
      "portal_shots/05_console_draft.jpg", "portal_shots/09_send_blocked.jpg"),
    N("2.06", "The public log shows each request, its due date, its status, and every response. Email addresses are "
              "never shown. A requester's name appears only if they choose. And text that may identify a student is "
              "held back until staff publish a redacted copy.",
      "portal_shots/10_log_list.jpg", "portal_shots/11_log_detail_response.jpg", "portal_shots/12_log_held.jpg"),
    N("2.07", "The software passes fifty-six automated tests. An independent review found nineteen defects, and all "
              "of them were fixed. Two steps remain before a pilot. The District's counsel should review the legal "
              "citations and the response templates. And the Claude step, tested so far with a stand-in, needs one "
              "live test.",
      "cards/status.png"),

    # ---------------------------------------------------------------- Part 3
    N("3.01", "Why Anthropic? The drafting step can use Anthropic's model, and that use costs money. The project does "
              "not want that cost to fall on the District's budget.",
      "cards/why.png"),
    N("3.02", "In October of twenty twenty-six, Anthropic filed papers to become a public company. In that filing, it "
              "says its public benefit work may include programs designed to make Claude accessible to underserved "
              "communities, educators, and public institutions. It has also placed five percent of its shares in a "
              "public benefit fund.",
      "cards/s1.png|push"),
    N("3.03", "So the project plans to ask Anthropic for two things. The first is use of Claude at no charge. The "
              "second is an operating grant to the proposed operator, Claremont Community Television, also known as "
              "the Claremont Community Media Center.",
      "cards/ask.png"),
    N("3.04", "Anthropic has made no commitment. If the answer is no, the portal still works, because the fixed rules "
              "can draft responses without Claude.",
      "cards/ask2.png"),
    N("3.05", "We are asking the Board and the Administration for a small set of decisions. The first is whether to "
              "run a pilot. The briefing that goes with this video lists the rest.",
      "cards/decisions.png"),
    N("3.06", "The portal drafts. District staff decide. Thank you for your time.",
      "cards/closing.png"),

    dict(id="END", kind="hold", secs=5.0, pics=["cards/end.png"]),
]
