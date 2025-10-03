const LOCAL_STORAGE_KEY = 'doreanreceipts';

class Tweet {
  constructor(handle, datetime, content) {
    this.handle = handle;
    this.datetime = datetime;
    this.content = content;
  }

  toString() {
    return `@${this.handle}\n${this.datetime.toLocaleString()}\n${this.content}`;
  }

  toJson() {
    return {
      handle: this.handle,
      datetime: this.datetime.toISOString(),
      content: this.content
    };
  }
}

const dump = (tweets) => JSON.stringify(Object.values(tweets).map(tweet => tweet.toJson()));

const download = (tweets) => {
  const blobData = dump(tweets);
  const blob = new Blob([blobData], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'doreanreceipts.json';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

const scrapeTweets = (tweets) => {
  const articles = document.querySelectorAll('article');
  articles.forEach(article => {
    const post = article.querySelector('div > div > div:nth-child(2) > div:nth-child(2)');
    const handleNode = post.children[0].querySelector('a');
    const handle = handleNode.href.split('/').pop();
    const timestamp = post.querySelector('time').getAttribute('datetime');
    const datetime = new Date(timestamp);
    const tweetNode = post.querySelector('[dir="auto"]');
    const tweet = new Tweet(handle, datetime, tweetNode.textContent);
    tweets[tweet.toString()] = tweet;
  });
};

const scrape = () => {
  const tweets = {}
  const savedTweets = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY) || '[]');
  savedTweets.forEach(tweet => {
    const savedTweet = new Tweet(tweet.handle, new Date(tweet.datetime), tweet.content);
    tweets[savedTweet.toString()] = savedTweet;
  });
  const scrollStep = window.innerHeight;
  const scrollInterval = 1000;
  const scrollAndScrape = () => {
    if (window.innerHeight + window.scrollY >= document.body.scrollHeight) {
      scrapeTweets(tweets);
      localStorage.setItem(LOCAL_STORAGE_KEY, dump(tweets));
      download(tweets);
      window.location.reload();
      return;
    }
    window.scrollBy(0, scrollStep);
    scrapeTweets(tweets);
    setTimeout(scrollAndScrape, scrollInterval);
  }
  scrollAndScrape();
}

setTimeout(scrape, 60 * 1000);