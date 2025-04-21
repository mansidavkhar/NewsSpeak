import requests
import pyttsx3
import threading


def fetch_news(country="us"):
    api_key = "77867cbf40154273ae07cd599cccf6d2"
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
    print(f"Requesting URL: {url}")
    
    response = requests.get(url)
    print(f"Response status code: {response.status_code}")
    
    if response.status_code == 200:
        news_data = response.json()
        print(f"Response structure: {news_data.keys()}")
        articles = news_data.get('articles', [])
        print(f"Number of articles: {len(articles)}")
        
        if articles:
            print(f"First article sample: {articles[0]}")
            titles = [article['title'] for article in articles]
            print(f"First few titles: {titles[:3]}")
            return titles
        else:
            print("No articles found in response")
    else:
        print(f"Error response: {response.text}")
    
    return []


def convert_text_to_speech(text):
    print(f"TTS requested for: {text}")
    
    def tts_thread(text):
        try:
            print("Initializing TTS engine...")
            engine = pyttsx3.init()
            print("TTS engine initialized")
            print("Setting up TTS...")
            engine.say(text)
            print("Starting TTS playback...")
            engine.runAndWait()
            print("TTS playback completed")
        except Exception as e:
            print(f"Error during TTS: {e}")
    
    print("Starting TTS thread")
    thread = threading.Thread(target=tts_thread, args=(text,))
    thread.start()
    print("TTS thread started")


def truncate_headlines(headlines, max_length=80):
    return [h if len(h) <= max_length else h[:max_length] + "..." for h in headlines]


def main():
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.label import Label

    class NewsApp(App):
        def build(self):
            layout = BoxLayout(orientation='vertical')
            fetch_news_btn = Button(text="Fetch News", size_hint=(1, 0.1))
            fetch_news_btn.bind(on_press=self.on_fetch_news)
            layout.add_widget(fetch_news_btn)

            self.news_box = BoxLayout(orientation='vertical', size_hint_y=None)
            self.news_box.bind(minimum_height=self.news_box.setter('height'))
            scroll_view = ScrollView(size_hint=(1, 0.9))
            scroll_view.add_widget(self.news_box)
            layout.add_widget(scroll_view)

            return layout

        def on_fetch_news(self, instance):
            self.news_box.clear_widgets()
            print("Fetching news...")
            headlines = fetch_news()
            print(f"Headlines fetched: {len(headlines)}")
            headlines = truncate_headlines(headlines)
            print(f"Headlines after truncation: {len(headlines)}")
            
            if headlines:
                print("Adding headlines to UI")
                for headline in headlines:
                    label = Label(text=headline, size_hint_y=None, height=40)
                    label.bind(on_touch_down=self.on_label_touch)
                    self.news_box.add_widget(label)
            else:
                print("No headlines fetched")

        def on_label_touch(self, instance, touch):
            if instance.collide_point(*touch.pos):
                print(f"Label touched: {instance.text}")
                convert_text_to_speech(instance.text)
                return True
            return False

    NewsApp().run()


if __name__ == "__main__":
    main()