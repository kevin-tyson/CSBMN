# Single source for the "Claude as mediator of district knowledge" explainer.
# Edit narration or pictures here, then run _source/make_cards.py (if a card changed),
# _source/make_docs.py and build_video.py.
#
# Segment kinds
#   hold : a still with no narration, held for `secs`
#   narr : one paragraph of narration, read by ElevenLabs; `pics` share its length
#
# A picture is "file" or "file|push" (slow push-in). Paths are relative to this folder.
# cards/ are drawn by _source/make_cards.py. portal_shots/ are reused from the RTK explainer:
# real screens of the RTK Portal on invented test data, each stamped TEST DATA.

TITLE = "Claude as the Front Desk for Claremont School District Records"
NAME = "Mediation-explainer"
SIZE = (1920, 1080)
FPS = 30
PARTS = {1: "Who is owed what", 2: "How Claude would mediate", 3: "Safeguards and a path",
         4: "Self-government and the appeal"}

def N(sid, text, *pics):
    return dict(id=sid, kind="narr", part=int(sid.split(".")[0]), text=text, pics=list(pics))

SEGMENTS = [
    dict(id="T0", kind="hold", secs=4.0, pics=["cards/title.png"]),

    # ---------------------------------------------------------------- Part 1
    N("1.01", "This video describes a proposal for the Claremont School District. The idea is to use Claude, an A-I "
              "model made by Anthropic, to help the district answer the people it serves, on time and within the law. "
              "It also explains why the project is asking Anthropic for support.",
      "cards/title.png", "cards/oneline.png"),
    N("1.02", "A school district owes information to many people, and the rules differ for each. Taxpayers and the "
              "public may inspect governmental records under New Hampshire's Right-to-Know Law. When a record is not "
              "immediately available, the district has five business days to respond.",
      "cards/constituents.png|push"),
    N("1.03", "Parents may see their own child's education records. Three laws set three deadlines for that: "
              "forty-five days under federal rule, fourteen days under one state law, and ten business days under a "
              "newer state law. A careful system follows the shortest.",
      "cards/clocks.png"),
    N("1.04", "Students take over those rights at eighteen. Former students can ask for their own records for as long "
              "as the district keeps them. Teachers and staff need the policies that govern their work, including the "
              "version that was in force on a given date.",
      "cards/constituents.png"),
    N("1.05", "The record is large. The School Board's policy index lists two hundred eighty-four policies, and one "
              "hundred twenty of them are dated before twenty fifteen. The archive of recorded meetings holds three "
              "hundred nineteen recordings. A resident with one free evening cannot read all of that.",
      "cards/volume.png"),
    N("1.06", "That has consequences. In August of twenty twenty-five, the Board announced a deficit then estimated at "
              "up to five million dollars. Yet the Board had been told at public meetings in twenty eighteen and twenty "
              "nineteen that its audits were years behind. Those warnings were on the public record, in hours of video "
              "that few residents had watched.",
      "cards/warning.png|push"),

    # ---------------------------------------------------------------- Part 2
    N("2.01", "Here is the proposed design. Every question, from any channel, passes through the same four layers. "
              "Every step is written to a log.",
      "cards/arch.png"),
    N("2.02", "First, a gate. It is made of fixed rules, not a model. It decides who is asking, which privacy tier the "
              "request falls in, and which legal deadline applies. A public question needs no sign-in. A request for a "
              "person's own records is verified by staff.",
      "cards/arch_gate.png"),
    N("2.03", "Second, the district's records graph. It holds public records only: every dated version of each "
              "policy, minutes, budgets, the index of recorded meetings, and each legal duty with its deadline and "
              "owner. Student and employee files stay in the district's own systems. They never enter the graph.",
      "cards/arch_graph.png"),
    N("2.04", "Third, Claude. It searches the graph and answers in plain language, with a link to the minute, policy "
              "or recording behind each statement. When the graph holds nothing on point, Claude says so, and offers "
              "to open a records request.",
      "cards/arch_claude.png"),
    N("2.05", "Fourth, a person. Where the law calls for a decision, Claude only drafts. A records custodian reads, "
              "edits and sends every response, and a draft with a blank left in it cannot be sent. The project's "
              "Right-to-Know portal already works this way. These screens show it running on invented test requests.",
      "cards/arch_custodian.png", "portal_shots/05_console_draft.jpg", "portal_shots/09_send_blocked.jpg"),
    N("2.06", "Last, the log. Every request, answer, review and release is recorded in a chain that shows whether any "
              "entry was later changed. The public part of the log lists each request, its due date, and its response.",
      "cards/arch_log.png", "portal_shots/10_log_list.jpg|push"),

    # ---------------------------------------------------------------- Part 3
    N("3.01", "The district's own policies set conditions that come first. Its policy on generative A-I requires the "
              "Superintendent's written approval before any A-I tool enters district systems. Its data governance "
              "policy requires the security officer to approve the vendor, even for a free service. The project's "
              "records show neither approval yet.",
      "cards/conditions.png"),
    N("3.02", "Federal privacy rules let an outside company handle student records only under the district's direct "
              "control. That is a question for the district's lawyer. Until it is answered, Claude would see public "
              "records only.",
      "cards/conditions.png|push"),
    N("3.03", "A mediator is also a gatekeeper. Whoever runs it shapes what people find. The design limits that power. "
              "Answers link to the original records, so anyone can check them. The log is public. The meeting "
              "navigator stays independent of the district. And the portal can draft responses with no model at all, "
              "so the district never depends on one company.",
      "cards/gatekeeper.png"),
    N("3.04", "The proposal starts small. Stage one answers questions about the public record. Stage two helps staff "
              "find the policy in force and draft routine letters. Stage three routes requests for a person's own "
              "records to staff, without the model reading them. Classroom use would come later, under the district's "
              "A-I plan, and is not part of this request.",
      "cards/stages.png"),
    N("3.05", "Nobody yet knows whether wide use of A-I will raise achievement in Claremont, and this proposal does not "
              "claim it. What a pilot can measure is narrower: answers given on time, sources that check out, how often "
              "staff change a draft, and what each answer costs.",
      "cards/measures.png"),

    # ---------------------------------------------------------------- Part 4
    N("4.01", "Why does this matter beyond one office? In Claremont, the voters act as the school district's "
              "legislature. In February of twenty twenty-six, residents debated the budget for four hours at the "
              "deliberative session. In March, they decided it by ballot. Each of those votes assumed that voters could "
              "find out what the district had done.",
      "cards/voters.png"),
    N("4.02", "New Hampshire's constitution says government should be open, accessible, accountable and responsive, "
              "and that public access to its records shall not be unreasonably restricted. The Right-to-Know Law begins "
              "by calling openness essential to a democratic society.",
      "cards/constitution.png|push"),
    N("4.03", "In eighteen thirty-five, Alexis de Tocqueville wrote that town meetings are to liberty what primary "
              "schools are to science. They put self-government within reach. That worked when a farmer could know the "
              "town's business first-hand. A district with a budget near forty-three million dollars, and recordings "
              "back to twenty fifteen, is past that point. Search with cited answers can bring the record back within "
              "reach.",
      "cards/tocqueville.png"),
    N("4.04", "Claremont has led before. Its name is on the nineteen ninety-three decision holding that the state must "
              "provide an adequate education and guarantee its funding. A district with a median household income of "
              "about fifty-four thousand dollars changed the rule for the whole state.",
      "cards/precedent.png"),
    N("4.05", "That is why the project is writing to Anthropic. In its October twenty twenty-six registration "
              "statement, Anthropic says its public benefit work may include programs designed to make Claude "
              "accessible to underserved communities, educators, and public institutions. It also placed five percent "
              "of its shares in a public benefit fund.",
      "cards/s1.png|push"),
    N("4.06", "The draft letter asks for two things: use of Claude at no charge during a pilot, and an operating grant "
              "to a nonprofit operator. In return, the project would publish what it measures, failures included. "
              "Anthropic has made no commitment, and the filing describes no application process.",
      "cards/ask.png"),
    N("4.07", "Some things must happen before the letter is sent. The district has to approve the tool, counsel has to "
              "review the design, and the sender should be a nonpartisan organization. The full proposal and its "
              "sources are in the written document that goes with this video.",
      "cards/before.png"),
    N("4.08", "Rules decide who may see what. Claude finds and drafts. People decide. Thank you for watching.",
      "cards/closing.png"),

    dict(id="END", kind="hold", secs=5.0, pics=["cards/end.png"]),
]
