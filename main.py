from email_sender import *
from transcript_fetcher import *
logging.basicConfig(filename='emails_sent.log', level=logging.DEBUG, format='%(asctime)s %(message)s')


def main():
    fetcher = TranscriptFetcher()
    messenger = Messenger()
    transcripts = fetcher.get_transcripts()
    for episode in transcripts:
        if messenger.send_string(episode.title, episode.transcript):
            logging.info("sent the episode: " + episode.title + ' ' + str(episode.first_page().url))
        else:
            logging.info("didn't send episode (found in previous episodes file)")

if __name__ == '__main__':
    main()
