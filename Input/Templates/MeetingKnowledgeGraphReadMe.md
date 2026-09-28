-   # Meeting Knowledge Graph
    

## Read Me First

A meeting is a nexus of the following resource:

-   A URL that identifies a Comcast video resource. 
    - The URL is discovered via either API or Google Chrome access to the CCMC VOD website.
-   A list of associated documents including, Agendas, Minutes, and any other files included in the meeting's packets. The URLs of the school district's online published files.
    - The URLs are discovered via either API or Google Chrome access to the distirict's online document store, currently Google Drive.
-   A full POSIX path to the local dialogue, diarized transcript, resource.

And has the following properties:

-   Date
-   Organization, e.g., **Claremont School Board**, **Unit School Board**, **SAU#6 School Board**, or named subcommittees thereof.
-   Location.
-   Participants and their roles.

The knowledge graph is externalized as the following CSV files: 

-   MeetingsKG.CSV, a catalog of meetings
-   CSBPolicies.PDF, a single file copy of the current policies obtained via Chrome accesss to the district's Google Drive documents.
-   SAU#6Policies.PDF
- Bylaws

The goal is for these files to provide the basis for a desktop AI agent system such as Coword and Codex to reason over the complete set of source documents that describe the actors and their actions that presaged what obtains in the Claremont School District.

## Processing Flow ##
1. Create PDF snapshot of policies via Google Chrome.
2. Download a copy of the Bylaws.
3. Download the Packets and Minutes.
3. Download _new_ MP4 meeting files.
4. Create JSON transcript files from the _new_ MP4 files using Adobe Premier
5. Create diarized dialogues from the transcripts.
5. For each new meeting:
    1. Find the URL for the Comcast VOD for the meeting using local Chrome or the API.
   2. Find the URLs for the district's published documents associated with this meeting using local Chrome or the API.
    3. Update MeetingsKG.CSV with the new meeting information.
   4. 