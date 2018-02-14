import boto3

client = boto3.client('ses')

smell = {
    "TemplateName": "intervention-ninja-smell",
    "SubjectPart": "Intervention Ninja - personal message to you",
    "HtmlPart": "<h3>Dear Friend,</h3><p>one of the <a href=\"http://www.intervention.ninja\" target=\"_blank\">"
                "Intervention Ninja</a> users thinks, <strong>that you might have a problem with hygiene...</strong> "
                "<br /><br />Is that true? You might not even realize that... <br /><br />Please don't be mad, it's "
                "very difficult to tell someone in person. Your coworker choose this secret way, so you can do "
                "something about it. <br /><br />Here - read some <a href=\"https://www.google.cz/search?q=facts%20"
                "coworker%20hygiene%20issues\" target=\"_blank\">facts about office hygiene issues.</a><br /><br />"
                "The first step to understanding your problem is to be honest with yourself and evaluate your symptoms "
                "without bias.<br /><br /></p><p>Best Regards, <br />Intervention Ninja<br /><br />PS: Do you think "
                "that someone else might need help to? Let them know - <strong>"
                "<a href=\"http://www.intervention.ninja\" target=\"_blank\">Intervention Ninja</a></strong>.</p>",
    "TextPart": "Dear Friend, one of the Intervention Ninja users thinks, that you might have a problem with "
                "hygiene... Is that true? You might not even realize that... Please don't be mad, it's very "
                "difficult to tell someone in person. Your coworker choose this secret way, so you can do "
                "something about it. Here - read some "
                "https://www.google.cz/search?q=facts%20coworker%20hygiene%20issues. The first step to "
                "understanding your problem is to be honest with yourself and evaluate your symptoms without bias. "
                "Best Regards, Intervention Ninja PS: Do you think that someone else might need help to? "
                "Let them know - http://www.intervention.ninja."
}

response = client.create_template(Template=smell)

print(response)

drink = {
    "TemplateName": "intervention-ninja-drink",
    "SubjectPart": "Intervention Ninja - personal message to you",
    "HtmlPart": "<h3>Dear Friend,</h3><p>one of the <a href=\"http://www.intervention.ninja\" target=\"_blank\">"
                "Intervention Ninja</a> users thinks, <strong>that you drink too much!</strong> "
                "<br /><br />Is that true? You might not even realize that... However it's more common than "
                "you think! Alcohol is the most highly abused drug in the United States. <br /><br />Here - "
                "read some <a href=\"https://www.google.cz/search?q=facts%20about%20alcoholism\" target=\"_blank\">"
                "facts about alcoholism.</a><br /><br />The first step to understanding your alcohol addiction "
                "is to be honest with yourself and evaluate your symptoms without bias. Take note of how much you "
                "are drinking, and talk to your loved ones about how they feel about your drinking.<br /><br /><strong>"
                "It's never too late!</strong></p><p>Best Regards, <br />Intervention Ninja<br /><br />PS: Do you "
                "think that someone else might need help to? Let them know - <strong>"
                "<a href=\"http://www.intervention.ninja\" target=\"_blank\">Intervention Ninja</a></strong>.</p>",
    "TextPart": "Dear Friend, one of the Intervention Ninja users thinks, that you drink too much!"
                "Is that true? You might not even realize that... However it's more common than you think! "
                "Alcohol is the most highly abused drug in the United States. Here - read some "
                "https://www.google.cz/search?q=facts%20about%20alcoholism. The first step to understanding your "
                "alcohol addiction is to be honest with yourself and evaluate your symptoms without bias. "
                "Take note of how much you are drinking, and talk to your loved ones about how they feel about "
                "your drinking. It's never too late! Best Regards, Intervention Ninja PS: Do you think that "
                "someone else might need help to? Let them know - http://www.intervention.ninja."
}


response = client.create_template(Template=drink)

print(response)
