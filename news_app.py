import requests
import pyttsx3
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label


class NewsApp(App):

    def fetch_news(self):
        url = ('https://newsapi.org/v2/top-headlines?'
               'country=us&'
               'apiKey=YOUR_API_KEY')
        
        response = requests.get(url)
        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get('articles', [])
            headlines = [article['title'] for article in articles]
            return headlines
        else:
            return []

    def convert_text_to_speech(self, text):
        def tts_thread(text):
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"Error during TTS: {e}")
        
        # Run the TTS in a separate thread to avoid blocking the main thread
        threading.Thread(target=tts_thread, args=(text,)).start()

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Button to fetch news
        fetch_news_btn = Button(text="Fetch News", size_hint=(1, 0.1))
        fetch_news_btn.bind(on_press=self.on_fetch_news)
        layout.add_widget(fetch_news_btn)

        # Scrollable area for news headlines
        self.news_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.news_box.bind(minimum_height=self.news_box.setter('height'))
        scroll_view = ScrollView(size_hint=(1, 0.9))
        scroll_view.add_widget(self.news_box)

        layout.add_widget(scroll_view)
        return layout

    def on_fetch_news(self, instance):
        self.news_box.clear_widgets()
        headlines = self.fetch_news()
        if headlines:
            for headline in headlines:
                label = Label(text=headline, size_hint_y=None, height=40)
                label.bind(on_touch_down=self.on_label_touch)
                self.news_box.add_widget(label)
        else:
            print("No headlines fetched")

    def on_label_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print(f"Label touched: {instance.text}")
            # Run TTS when a label is touched
            self.convert_text_to_speech(instance.text)
            return True
        return False


if __name__ == "__main__":
    NewsApp().run()
