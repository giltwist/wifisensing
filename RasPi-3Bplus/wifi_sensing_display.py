# This is NOT stand-alone code, this is the most relevant portion
# of my Kivy-powered UI to help illustrate how raw RSSI can be
# made into something more useful, like a motion alarm

import numpy as np
from kivy_garden.graph import Graph, MeshLinePlot


    # generates a nice little RSSI v time graph in Kivy
    def _build_wifi_sensing_popup(self):
        self.pop = Popup(title='Motion Sensing: Initializing', size_hint=(1, 1), auto_dismiss=False)
        self.box = BoxLayout(orientation='vertical');

        self.graph = Graph(xlabel='Time',
        x_ticks_major=10, y_ticks_major=.25,
        y_grid_label=False, x_grid_label=False, padding=1,
        x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-0, ymax=1)

        self.base_plot = MeshLinePlot(color=[1, 1, 1, 1])
        self.graph.add_plot(self.base_plot)

        self.smoothed_plot = MeshLinePlot(color=[0, 0, 1, 1])
        self.graph.add_plot(self.smoothed_plot)

        self.alert_plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.graph.add_plot(self.alert_plot)

        self.label = Label(text='[color=ffffff]RSSI[/color] [color=0000ff]Smooth[/color] [color=ff0000]Motion[/color]', markup=True, size_hint_y=.1)

        self.box.add_widget(self.label)
        self.box.add_widget(self.graph)

        self.Tslider = Slider(min = 0.0, max = 1.0, value = 0.6, step=0.01, size_hint_y=0.1)
        self.box.add_widget(self.Tslider)
        self.Tslider.bind(value = self.on_threshold_change)

        self.Tlabel = Label(text = "0.6", size_hint_y=0.1)
        self.box.add_widget(self.Tlabel)

        self.Sslider = Slider(min = 1, max = 20, value = 5, step=1, size_hint_y=0.1)
        self.box.add_widget(self.Sslider)
        self.Sslider.bind(value = self.on_smoothing_change)

        self.Slabel = Label(text = "5", size_hint_y=0.1)
        self.box.add_widget(self.Slabel)

        self.pop.content=self.box
        return self.pop

    # Does a rolling box average of size smoothing
    # Determines if current reading exceeds threshold stdevs from that mean
    # Smoothing and threshold are just int sliders in my UI from 1 to 10
    # Noisy/Busy networks need more smoothing and a higher threshold
    def update_wifisensing(self, instance):
        deck = self.rx.getDeck()
        index = range(len(deck))

        smoothing = int(self.smoothing)
        threshold = self.threshold
        offset=int(smoothing/2)
#        print(str(smoothing)+"|"+str(threshold))
        base_series = list(zip(index, deck))
        self.base_plot.points=base_series

        if len(deck)>2*smoothing:

            smooth = np.convolve(deck,np.ones(smoothing))/smoothing
#            print(len(smooth[offset:-offset]))

            smoothed_series = list(zip(index, smooth[offset:-offset]))
            self.smoothed_plot.points=smoothed_series

            mean = np.average(smooth)
            sd = max(0.001,np.std(smooth))

            alert = (mean-np.array(smooth))/sd
#            print(len(alert))
            alert_series = list(zip(index[2:-2], alert[offset+2:-offset-2]))
            self.alert_plot.points=alert_series

            if self._wifi_sensing_active:
                #print(alert[smoothing:-smoothing])
                if max(alert[smoothing:-smoothing])>threshold:
                    self.mqtt.publish(TOPIC_SET_LAMP_CONFIG,json.dumps(self.red_state).encode('utf-8'),qos=1)
                    self.wifi_sensing_popup.title="MOTION DETECTED!"
                else:
                    self.mqtt.publish(TOPIC_SET_LAMP_CONFIG,json.dumps(self.green_state).encode('utf-8'),qos=1)
                    self.wifi_sensing_popup.title="Motion Sensing: Active"

        Clock.schedule_once(lambda dt: self.update_wifisensing(instance), 0.1)
