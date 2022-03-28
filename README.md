# PaohRasaPlatform

# Introduction

This repository contains Botfront Dockers for running the Botfront locally and to e.g. develop new Rasa Actions to be used in the chatbot.

Botfront is an open source graphical UI for developing and maintaining Rasa chatbots. Read more from [Botfront docs](https://botfront.io/docs/rasa/getting-started/) and [Rasa docs](https://rasa.com/docs/rasa/)

# Getting Started Locally

Firstly, download file`lid.176.bin` from https://fasttext.cc/docs/en/language-identification.html to `rasa/auto_lang_detect` directory

Start Botfront locally at the first time:
1.	Install Docker if not already installed
2.  Install Python if not already installed
3.  On the command line run `python generate_compose_env_file.py` to generate Botfront env file for Dockers (if you don't have Python, you could copy needed env vars from the Python script and create the file manually)
4.	On the command line run `docker-compose -f docker-compose.local.yml up -d` to start Botfront (use the `local` version of docker-compose files)
5.	Open `http://localhost:8888/` on your browser (wait little time after docker-compose up if not responding)
6.	On Admin Settings `http://localhost:8888/admin/settings/default-nlu-pipeline`, comment away the `#- name: rasa_addons.nlu.components.gazette.Gazette` row in Default NLU Pipeline (there seems to be bug in current Botfront version when training new NLU model with Gazette)
7.  Add new project in `http://localhost:8888/admin/projects` (you can also delete the already existing chitchat project)
8.  Copy your project id and replace the existing id in `BF_PROJECT_ID` field in the `.env` file
9. Restart Botfront by running `docker-compose -f docker-compose.local.yml up -d` on the command line
10. Click your project's name to open the project in `http://localhost:8888/admin/projects`
11. Clone `BotfrontChatbotProject` repository somewhere in your local machine
12. Create `.zip` file of the cloned repository's `BotfrontChatbotProject` folder
13. Go to project settings in Botfront, select `Import/Export` and add the `.zip` file in the Import tab
14. Turn on the `Reset project` toggle to make sure possible existing project won't conflict with the import
15. In order for bot to respond to your message, you need to train it first. Press button 'train' in the upper right corner of Botfront UI to do this.
16. Now you should have local version of the chatbot
17. You can shutdown the Botfront by running `docker-compose -f docker-compose.local.yml down` on the command line

Next time, you can start Botfront again by running `docker-compose -f docker-compose.local.yml up -d` on the command line

# Deploying to Azure cloud

The docker images are deployed to the test and production environments from `dev` and `main` branches respectively. The pipeline uses Azure Container registry to store created images and later deploys them to run as containers in AKS cluster under Private Network in Azure. The connection credentials are a part of the pipeline and those are fetched from Azure Key Vault.

To run the deployment it is enough to merge to `dev` and `main` branches after which tests are run and if those succeed the new version is deployed.

The Azure Devops pipeline is defined in `azure-pipelines.yml` file and AKS Kubernetes configs are in `kube/` folder.


# Development locally

## How to build Rasa and Rasa Actions Dockers locally

You can build Rasa and Rasa Actions docker images by running `docker compose -f docker-compose.local.yml build`.

You can start Rasa and Rasa Actions locally using the Docker Compose:
1. This Rasa is modified for Botfront so you need to have Botfront running first so that Rasa can fetch configs from Botfront on the startup. Check the [Botfront repository](https://dev.azure.com/turunkaupunki/VmPalvelukonsolidaatio/_git/Botfront) on how to start it locally.
2. Check that your `.env` file has the correct local Botfront URL port in the `BF_URL` variable (should be 3000 by default) and put your Botfront project ID (you can copy if from the Botfront Admin Projects menu UI) into `BF_PROJECT_ID` variable
3.	On the command line run `docker compose -f docker-compose.local.yml up -d` to start Rasa and Rasa Actions (use the `local` version of docker-compose files)
4. You can shutdown containers by running `docker compose -f docker-compose.local.yml down` on the command line

# Custom Rasa modifications made for Palveluohjaaja

Custom Rasa modifications made for Palveluohjaaja can be found from the `rasa` folder. Currently, there are three different modifications called `anonymized_tracker_store`, `auto_lang_detect` and `fallback_service_search` which are used in Palveluohjaaja.

## anonymized_tracker_store

This modification contains customized Rasa tracker store for Botfront that anonymizes personally identifiable information from Rasa conversation logs before they get stored in persistent database. Currently replaces only phone numbers, IP addresses and Finnish social security numbers with appropriate tags.

To use this anonymized tracker store in your Botfront project:
1. If you are running this Botfront locally, rebuild Rasa container if you have built it before
2. Go to Botfront project settings `Endpoints` tab and change `store_type` to `anonymized_tracker_store.botfront_anonymized_tracker_store.BotfrontAnonymizedTrackerStore` under `tracker_store` section
3. Restart Rasa container

## auto_lang_detect

This modification contains customized Botfront's webchat channel for Rasa used to integrate web front-end's chatwidget to Rasa. It has two modifications for Palveluojaaja-botti: automatic language detection of the user's message, and functionality to inform the front-end about changed municipality slot value.

### Automatic language detection

Palveluohjaaja has feature that it can change the bot's response language on the fly if user changes their language during conversation. This can happen if user explicitly changes language from the front-end's language selector or by detecting the changed language from user's messages.

For detecting the language of the user's message, this modification uses [FastText's Language Identification](https://fasttext.cc/docs/en/language-identification.html) Python library. The needed FastText model `lid.176.bin` is included in this repository.

The code for detecting user's language is in `rasa/auto_lang_detect/webchat.py` file on rows 257-296. The code will check that the user's message needs to have at least two words, not start with "/" (which is used in messages when user clicks bot's buttons), detected language confidence must be at least 40% and the detected language must be Finnish, Swedish or English (which are the supported languages of the Palveluohjaaja).

If all those requirements are fulfilled and the detected language is different from the previosly used language, bot's language will be changed. Also, Rasa will emit socketio event `bot_language_changed` to the web front-end so the front-end will also update its language accordingly.

### Inform front-end about changed municipality slot value

Palveluohjaaja's web front-end has feature that it will show user's selected municipality filter and the selection can also be removed from the front-end. Rasa will detect wanted municipality with its entity recognition from the the user's message and store the recognized municipality to Rasa's `municipality` slot. If Rasa will detect updated municipality entity from user's new message, front-end needs to be notified about the change so that it can show the correct municipality value.

This is implemented in `rasa/auto_lang_detect/webchat.py` file on rows 39-54 where Rasa will send new bot responses through the webchat output channel to the front-end. If Rasa's entity recognition has detected new municipality, it's valid municipality for Palveluohjaaja (there is a list of accepted municipalities in `rasa/auto_lang_detect/webchat.py`), and the detected value is different from the previous value, Rasa will emit socketio event `bot_municipality_changed` to the web front-end so the front-end will also update its municipality accordingly.

Note: to get the recognized municipality slot value to the webchat output channel message metadata, it has been added to the output message's metadata in `rasa/auto_lang_detect/graphql.py` on line 210.

## fallback_service_search

Palveluohjaaja has feature that if the Rasa cannot detect some predefined intent with high enough confidence, it will trigger free text service search using the Palveluohjaaja's Service Recommender. Thus, the bot will not say the traditional "Sorry I didn't understand" but it will send user's message to the Service Recommender to show suitable service recommendations based on the user's message.

This is implemented using Rasa's [NLU fallback](https://rasa.com/docs/rasa/2.x/fallback-handoff/#nlu-fallback) feature. Rasa's default `FallbackClassifier` component didn't seem to support defining custom intent name to be triggered from the NLU Fallback so there is a slightly modified version of the default `FallbackClassifier` in `rasa/fallback_service_search/fallback_service_search.py` file called `FallbackServiceSearchClassifier`. It should be enabled in Botfront's NLU Settings pipeline configuration as follows:

```yaml
- name: fallback_service_search.fallback_service_search.FallbackServiceSearchClassifier
  threshold: 0.6
  fallback_intent_name: fallback_service_search
```

With the `threshold` parameter you can set threshold for the NLU Fallback classifier. If the originally detected intent's confidence is under the defined threshold, `FallbackServiceSearchClassifier` will activate and trigger the intent defined in parameter `fallback_intent_name`. At Palveluohjaaja, there is own Rasa story for the fallback service recommendation which starts with intent `fallback_service_search`.

# Custom Rasa Actions made for Palveluohjaaja

Custom Rasa Actions made for Palveluohjaaja can be found from the `actions` folder. Rasa Actions are used for all bot actions that cannot be handled in the Botfront visual chatbot editor and require custom code. Actions enable the chatbot to run any custom code, including API calls, database queries etc.

Currently, most of the custom actions are used for recommending services with the Palveluohjaaja's Service Recommender in diffent conversation scenarios. There are also a few actions used to reset different Rasa slots. Then there are two more special actions in files `default_fallback_action.py` and `set_feedback_reminder_action.py` which are introduced below.

## default_fallback_action

Rasa's fallback feature is two staged: the first one is the "NLU Fallback" introduced earlier in the `fallback_service_search` section and the other stage is the "Core Fallback" which you can read more about at [Rasa's documentation](https://rasa.com/docs/rasa/2.x/fallback-handoff/#handling-low-action-confidence). Rasa's default Core Fallback Action just sends message to user but at Palveluohjaaja we want to trigger the free text service recommendation just as previously described in the `fallback_service_search` section. Thus, there is a custom Core Fallback Action created in the `default_fallback_action.py` file.

The custom action will deactivate any active form loops (which would infer with the upcoming service recommendation conversation path), update bot's language if user has changed that in the web front-end's menu, and finally it will set the user's latest message to `core_fallback_service_search_text` slot and trigger the intent `core_fallback_service_search`. At Palveluohjaaja, there is own Rasa story for the core fallback service recommendation which starts with intent `core_fallback_service_search`.

This custom Core Fallback Action should be enabled in Botfront's Dialogue -> Policies configuration as follows:

```yaml
- name: RulePolicy
  core_fallback_threshold: 0.6
  core_fallback_action_name: "action_custom_fallback"
  enable_fallback_prediction: True
```

## set_feedback_reminder_action

Palveluohjaaja has feature that if user doesn't reply anything in some time after the bot has asked feedback about its service recommendations, the bot will automatically send so called "back to start" message. This is implemented using Rasa's Reminder Action feature which you can read more about from [Rasa's documentation](https://rasa.com/docs/rasa/2.x/reaching-out-to-user/#reminders). Thus, there is a custom Reminder Action created in the `set_feedback_reminder_action.py` file.

The custom action will send reminder to Rasa in 25 seconds and trigger intent `EXTERNAL_feedback_reminder` if user hasn't responed anything before that. At Palveluohjaaja, there is own Rasa story for the "back to start" message which starts with intent `EXTERNAL_feedback_reminder`.