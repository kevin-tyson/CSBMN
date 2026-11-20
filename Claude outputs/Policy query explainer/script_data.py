# Single source for the "csb-policy-query: install and use" explainer.
# Edit narration or pictures here, then run _source/make_cards.py (if a card changed),
# _source/make_docs.py and build_video.py.
#
# Segment kinds
#   hold : a still with no narration, held for `secs`
#   narr : one paragraph of narration, read by ElevenLabs; `pics` share its length
#
# A picture is "file" or "file|push" (slow push-in). Paths are relative to this folder.
# cards/ are drawn by _source/make_cards.py. The two demo answers on the cards are the
# skill's real output for questions asked on November 20, 2026; policy text is quoted
# from the documents as the Google Drive connector returned them that day.

TITLE = "Asking Claude About Claremont School Board Policy"
SUBTITLE = "How to install and use the csb-policy-query skill"
NAME = "Policy-query-explainer"
SIZE = (1920, 1080)
FPS = 30
PARTS = {1: "What the skill does", 2: "Installing it", 3: "Using it"}

def N(sid, text, *pics):
    return dict(id=sid, kind="narr", part=int(sid.split(".")[0]), text=text, pics=list(pics))

SEGMENTS = [
    dict(id="T0", kind="hold", secs=4.0, pics=["cards/title.png"]),

    # ---------------------------------------------------------------- Part 1
    N("1.01", "This video shows how to install and use a skill for Claude called C-S-B policy query. A skill is a "
              "set of written instructions that Claude follows for one kind of task. This one answers questions "
              "about Claremont School Board policy.",
      "cards/title.png", "cards/what.png"),
    N("1.02", "The district publishes its policies through one Google document: an index with about three hundred "
              "fifty links, in twelve sections lettered A through L. Each link opens a policy, a regulation, or a "
              "form.",
      "cards/index.png|push"),
    N("1.03", "The skill answers from that index and the documents it links, and nothing else. It does not use "
              "news, meeting minutes, or what Claude already knows about New Hampshire law. When a policy cites a "
              "statute, the answer says so, but it does not say what the statute requires.",
      "cards/scope.png"),
    N("1.04", "Every statement in an answer names the policy behind it, with a link. And when the policies do not "
              "answer the question, the reply is two words: Insufficient Data.",
      "cards/promise.png"),

    # ---------------------------------------------------------------- Part 2
    N("2.01", "Installing it takes three steps. First, skills need code execution. On a Free, Pro or Max plan, open "
              "Settings, then Capabilities, and turn on Code execution and file creation. Newer versions of the "
              "settings page call it Create and edit files. On a Team or Enterprise plan, an owner has to allow "
              "skills for the organization first.",
      "cards/step1.png"),
    N("2.02", "Second, upload the skill. It comes as a zip file holding one folder with one instruction file. In "
              "Claude, open Customize, then Skills. Click the plus button, choose Create skill, then Upload a skill, "
              "and pick the zip file. The skill appears in your list with a switch. Make sure it is on. A skill you "
              "upload is private to your account.",
      "cards/step2.png"),
    N("2.03", "Third, connect Google Drive, because the policies live there. Open Customize, then Connectors, find "
              "Google Drive, choose Connect, and sign in with your Google account. Claude can open only the files "
              "that account can open. The index is shared with anyone who has the link, and so are the policies "
              "tested for this video.",
      "cards/step3.png"),

    # ---------------------------------------------------------------- Part 3
    N("3.01", "To use it, ask a question about school board policy in plain words. Claude picks the skill on its own "
              "when a question fits. Here are two real questions, asked on November twentieth, twenty twenty-six.",
      "cards/ask.png"),
    N("3.02", "The first: may students use their cell phones during lunch? Claude reads the index fresh, lists every "
              "entry, and looks for titles about phones, devices and lunch. It also searches Google Drive, and keeps "
              "only files the index links. Then it reads the strongest matches.",
      "cards/flow.png", "cards/flow_q1.png"),
    N("3.03", "The answer is no. Policy J-I-C-J, Unauthorized Communication Devices, adopted in September twenty "
              "twenty-five, bars student use of personal devices from the first bell to the dismissal bell. It says "
              "the school day includes lunch periods, passing time and recesses. It also lists exceptions for "
              "medical needs, disabilities and language access.",
      "cards/answer1.png", "cards/jicj_text.png|push"),
    N("3.04", "The answer also reports an older policy that is still in the index. J-I-C-A-B, from twenty ten, says "
              "permitted uses of electronic devices will be set out in the student and parent handbooks. Neither "
              "policy says it replaces the other, so the skill shows both, with their dates.",
      "cards/overlap.png"),
    N("3.05", "The second question: how many votes did each candidate get in the March twenty twenty-six school "
              "board election? The skill read policy B-B-B, on board membership and elections. It says board "
              "members are elected each March for three-year terms. It gives no results. The Drive search also "
              "turned up meeting minutes and an agenda, but those are not policies, so the skill set them aside.",
      "cards/q2.png"),
    N("3.06", "So the reply is: Insufficient Data. That tells you the answer is not in board policy, and you need "
              "another source, such as the election results.",
      "cards/answer2.png"),
    N("3.07", "Two more cases. If the policies answer only part of a question, the skill answers that part and "
              "marks the rest Insufficient Data. If a policy cannot be opened, it says which one, instead.",
      "cards/cases.png"),
    N("3.08", "One source. A policy behind every statement. Two words when the policies are silent. Thank you for "
              "watching.",
      "cards/closing.png"),

    dict(id="END", kind="hold", secs=5.0, pics=["cards/end.png"]),
]
