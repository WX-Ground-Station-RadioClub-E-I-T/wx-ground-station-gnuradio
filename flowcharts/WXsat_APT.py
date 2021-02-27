#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Desmodulador FM para NOAA
# Author: pepassaco
# GNU Radio version: 3.8.2.0

from datetime import datetime
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import doppler
import soapy
import distutils
from distutils import util


class WXsat_APT(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Desmodulador FM para NOAA")

        ##################################################
        # Variables
        ##################################################
        self.fcd_freq = fcd_freq = 137100000
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = fcd_freq
        self.samp_rate = samp_rate = 768000
        self.recfile2 = recfile2 = "/src/prueba2.wav"
        self.recfile = recfile = "/src/prueba1.wav"
        self.prefix = prefix = "/home/tallerine/sdr-apt/wav/"
        self.lna_gain_0 = lna_gain_0 = 30
        self.f_real = f_real = 1
        self.cutoff = cutoff = 40
        self.bpf_lp = bpf_lp = 500
        self.bpf_hp = bpf_hp = 5000
        self.antenna = antenna = "RX"
        self.af_gain = af_gain = 30

        ##################################################
        # Blocks
        ##################################################
        self.soapy_source_0 = None
        # Make sure that the gain mode is valid
        if('Overall' not in ['Overall', 'Specific', 'Settings Field']):
            raise ValueError("Wrong gain mode on channel 0. Allowed gain modes: "
                  "['Overall', 'Specific', 'Settings Field']")

        dev = 'driver=remote'

        # Stream arguments for every activated stream
        tune_args = ['']
        settings = ['']

        # Setup the device arguments
        dev_args = "remote=192.168.0.10:55132, remote:driver=airspyhf"

        self.soapy_source_0 = soapy.source(1, dev, dev_args, '',
                                  tune_args, settings, samp_rate, "fc32")



        self.soapy_source_0.set_dc_removal(0,bool(distutils.util.strtobool('False')))

        # Set up DC offset. If set to (0, 0) internally the source block
        # will handle the case if no DC offset correction is supported
        self.soapy_source_0.set_dc_offset(0,0)

        # Setup IQ Balance. If set to (0, 0) internally the source block
        # will handle the case if no IQ balance correction is supported
        self.soapy_source_0.set_iq_balance(0,0)

        # Setup Frequency correction. If set to 0 internally the source block
        # will handle the case if no frequency correction is supported
        self.soapy_source_0.set_frequency_correction(0,0)

        self.soapy_source_0.set_agc(0,False)

        self.soapy_source_0.set_frequency(0,"BB",0)

        self.soapy_source_0.set_frequency(0, fcd_freq)

        self.soapy_source_0.set_antenna(0,antenna)

        if('Overall' != 'Settings Field'):
            # pass is needed, in case the template does not evaluare anything
            pass
            self.soapy_source_0.set_gain(0,lna_gain_0)
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_fff(
                interpolation=20800,
                decimation=48000,
                taps=None,
                fractional_bw=None)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=96000,
                decimation=samp_rate,
                taps=None,
                fractional_bw=None)
        self.low_pass_filter_1_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                30,
                96000,
                cutoff*1000,
                500,
                firdes.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                10,
                20800,
                2000,
                500,
                firdes.WIN_HAMMING,
                6.76))
        self.hilbert_fc_0_0 = filter.hilbert_fc(5, firdes.WIN_HAMMING, 6.76)
        self.doppler_doppler_0 = doppler.doppler(40.4167, -3.70325, 666, 'ISS', '', 0.1, False)
        self.doppler_MsgPairToVar_0 = doppler.MsgPairToVar(self.set_freq_real)
        self.blocks_wavfile_sink_1_0 = blocks.wavfile_sink(recfile2, 1, 4160, 16)
        self.blocks_wavfile_sink_0_0 = blocks.wavfile_sink(recfile, 1, 20800, 16)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(af_gain)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_ff(11, 1/11., 4000, 1)
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 5)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(1)
        self.band_pass_filter_0 = filter.interp_fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                48000,
                bpf_lp,
                bpf_hp,
                200,
                firdes.WIN_HAMMING,
                6.76))
        self.analog_wfm_rcv_0_0 = analog.wfm_rcv(
        	quad_rate=96000,
        	audio_decimation=2,
        )
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, fcd_freq*(1-f_real), 1, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.doppler_doppler_0, 'dop_factor'), (self.doppler_MsgPairToVar_0, 'inpair'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_wfm_rcv_0_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_wavfile_sink_0_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.hilbert_fc_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_wavfile_sink_1_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_keep_one_in_n_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.hilbert_fc_0_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.low_pass_filter_1_0, 0), (self.analog_wfm_rcv_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_1_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.soapy_source_0, 0), (self.blocks_multiply_xx_0, 0))


    def get_fcd_freq(self):
        return self.fcd_freq

    def set_fcd_freq(self, fcd_freq):
        self.fcd_freq = fcd_freq
        self.set_variable_qtgui_label_0(self.fcd_freq)
        self.analog_sig_source_x_0.set_frequency(self.fcd_freq*(1-self.f_real))
        self.soapy_source_0.set_frequency(0, self.fcd_freq)

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_recfile2(self):
        return self.recfile2

    def set_recfile2(self, recfile2):
        self.recfile2 = recfile2
        self.blocks_wavfile_sink_1_0.open(self.recfile2)

    def get_recfile(self):
        return self.recfile

    def set_recfile(self, recfile):
        self.recfile = recfile
        self.blocks_wavfile_sink_0_0.open(self.recfile)

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix

    def get_lna_gain_0(self):
        return self.lna_gain_0

    def set_lna_gain_0(self, lna_gain_0):
        self.lna_gain_0 = lna_gain_0
        self.soapy_source_0.set_gain(0, self.lna_gain_0)

    def get_f_real(self):
        return self.f_real

    def set_f_real(self, f_real):
        self.f_real = f_real
        self.analog_sig_source_x_0.set_frequency(self.fcd_freq*(1-self.f_real))

    def get_cutoff(self):
        return self.cutoff

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff
        self.low_pass_filter_1_0.set_taps(firdes.low_pass(30, 96000, self.cutoff*1000, 500, firdes.WIN_HAMMING, 6.76))

    def get_bpf_lp(self):
        return self.bpf_lp

    def set_bpf_lp(self, bpf_lp):
        self.bpf_lp = bpf_lp
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, 48000, self.bpf_lp, self.bpf_hp, 200, firdes.WIN_HAMMING, 6.76))

    def get_bpf_hp(self):
        return self.bpf_hp

    def set_bpf_hp(self, bpf_hp):
        self.bpf_hp = bpf_hp
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, 48000, self.bpf_lp, self.bpf_hp, 200, firdes.WIN_HAMMING, 6.76))

    def get_antenna(self):
        return self.antenna

    def set_antenna(self, antenna):
        self.antenna = antenna
        self.soapy_source_0.set_antenna(0,self.antenna)

    def get_af_gain(self):
        return self.af_gain

    def set_af_gain(self, af_gain):
        self.af_gain = af_gain
        self.blocks_multiply_const_vxx_0_0.set_k(self.af_gain)





def main(top_block_cls=WXsat_APT, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
