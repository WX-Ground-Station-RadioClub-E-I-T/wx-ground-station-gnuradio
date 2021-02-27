#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Desmodulador QPSK
# Author: pepassaco
# Description: v4
# GNU Radio version: 3.8.2.0

from datetime import datetime
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import doppler
import numpy as np
import soapy
import distutils
from distutils import util


class WXsat_LRPT_no_gui(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Desmodulador QPSK")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_airspy = samp_rate_airspy = 768000
        self.interp = interp = 1
        self.decim = decim = 1
        self.symb_rate = symb_rate = 72000
        self.samp_rate = samp_rate = samp_rate_airspy/decim*interp
        self.sps = sps = (samp_rate*1.0)/(symb_rate*1.0)
        self.filterSize = filterSize = 8
        self.ruta_res = ruta_res = "/src/Resultados/Meteor/1_D"
        self.ruta_mal = ruta_mal = "/src/Resultados/Pruebas/Mala.raw"
        self.ruta_dec = ruta_dec = "/src/Resultados/Pruebas/Decente.raw"
        self.ruta_bien = ruta_bien = "/src/Resultados/Pruebas/Buena.raw"
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(filterSize, filterSize, 1.0/float(sps), 0.6, 45*filterSize)
        self.raw_file_d = raw_file_d = "/src/Resultados/Meteor/Meteor_d"+ datetime.now().strftime("%d%m%Y_%H%M")+"_D"
        self.raw_file = raw_file = "/src/Resultados/Meteor/Meteor_"+ datetime.now().strftime("%d%m%Y_%H%M")+"_R"
        self.pll_alpha = pll_alpha = 0.015
        self.lp_taps = lp_taps = firdes.low_pass(1.0, samp_rate_airspy, 55000,5000, firdes.WIN_HAMMING, 6.76)
        self.lp_corte = lp_corte = 60e3
        self.loopBW = loopBW = 6.28/80
        self.gain = gain = 30
        self.freq = freq = 137100000
        self.f_real = f_real = 1
        self.f_offset = f_offset = 200e3
        self.eqGain = eqGain = 0.008
        self.debug_2 = debug_2 = "/src/Resultados/Pruebas/conEQ.s"
        self.debug_1 = debug_1 = "/src/Resultados/Pruebas/sinEQ.s"
        self.bitstream_name = bitstream_name = "/src/Resultados/Meteor_"+ datetime.now().strftime("%d%m%Y_%H%M") + ".s"
        self.antenna = antenna = "RX"

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
                                  tune_args, settings, samp_rate_airspy, "fc32")



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

        self.soapy_source_0.set_frequency(0, freq+f_offset)

        self.soapy_source_0.set_antenna(0,antenna)

        if('Overall' != 'Settings Field'):
            # pass is needed, in case the template does not evaluare anything
            pass
            self.soapy_source_0.set_gain(0,gain)
        self.root_raised_cosine_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                symb_rate,
                0.6,
                64))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, lp_taps, -f_offset, samp_rate_airspy)
        self.doppler_doppler_0 = doppler.doppler(40.4167, -3.70325, 666, 'ISS', '', 0.1, False)
        self.doppler_MsgPairToVar_0 = doppler.MsgPairToVar(self.set_f_real)
        self.digital_symbol_sync_xx_0_0_0 = digital.symbol_sync_cc(
            digital.TED_GARDNER,
            sps,
            loopBW,
            0.7,
            1,
            0.01,
            1,
            digital.constellation_qpsk().base(),
            digital.IR_PFB_NO_MF,
            filterSize,
            rrc_taps)
        self.digital_costas_loop_cc_1_0_1 = digital.costas_loop_cc(pll_alpha, 4, False)
        self.digital_constellation_soft_decoder_cf_1 = digital.constellation_soft_decoder_cf(digital.constellation_calcdist(([-1-1j, -1+1j, 1+1j, 1-1j]), ([0, 1, 3, 2]), 4, 1).base())
        self.digital_cma_equalizer_cc_0 = digital.cma_equalizer_cc(16, 1, eqGain, 1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_cc(1.4142)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(0.707)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(5/4)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 127)
        self.blocks_file_sink_2 = blocks.file_sink(gr.sizeof_gr_complex*1, raw_file_d, False)
        self.blocks_file_sink_2.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, debug_2, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate_airspy, analog.GR_COS_WAVE, freq*(1-f_real), 1, 0, 0)
        self.analog_rail_ff_0 = analog.rail_ff(-1, 1)
        self.analog_agc_xx_0 = analog.agc_cc(1e-2, 1.2, 1.0)
        self.analog_agc_xx_0.set_max_gain(400000)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.doppler_doppler_0, 'dop_factor'), (self.doppler_MsgPairToVar_0, 'inpair'))
        self.connect((self.analog_agc_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.analog_rail_ff_0, 0), (self.blocks_float_to_char_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_float_to_char_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.digital_costas_loop_cc_1_0_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.analog_rail_ff_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.digital_constellation_soft_decoder_cf_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_constellation_soft_decoder_cf_1, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.digital_costas_loop_cc_1_0_1, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.digital_symbol_sync_xx_0_0_0, 0), (self.digital_cma_equalizer_cc_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.root_raised_cosine_filter_0_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.digital_symbol_sync_xx_0_0_0, 0))
        self.connect((self.soapy_source_0, 0), (self.blocks_file_sink_2, 0))
        self.connect((self.soapy_source_0, 0), (self.blocks_multiply_xx_0, 0))


    def get_samp_rate_airspy(self):
        return self.samp_rate_airspy

    def set_samp_rate_airspy(self, samp_rate_airspy):
        self.samp_rate_airspy = samp_rate_airspy
        self.set_samp_rate(self.samp_rate_airspy/self.decim*self.interp)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate_airspy)

    def get_interp(self):
        return self.interp

    def set_interp(self, interp):
        self.interp = interp
        self.set_samp_rate(self.samp_rate_airspy/self.decim*self.interp)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.set_samp_rate(self.samp_rate_airspy/self.decim*self.interp)

    def get_symb_rate(self):
        return self.symb_rate

    def set_symb_rate(self, symb_rate):
        self.symb_rate = symb_rate
        self.set_sps((self.samp_rate*1.0)/(self.symb_rate*1.0))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symb_rate, 0.6, 64))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sps((self.samp_rate*1.0)/(self.symb_rate*1.0))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symb_rate, 0.6, 64))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(self.filterSize, self.filterSize, 1.0/float(self.sps), 0.6, 45*self.filterSize))

    def get_filterSize(self):
        return self.filterSize

    def set_filterSize(self, filterSize):
        self.filterSize = filterSize
        self.set_rrc_taps(firdes.root_raised_cosine(self.filterSize, self.filterSize, 1.0/float(self.sps), 0.6, 45*self.filterSize))

    def get_ruta_res(self):
        return self.ruta_res

    def set_ruta_res(self, ruta_res):
        self.ruta_res = ruta_res

    def get_ruta_mal(self):
        return self.ruta_mal

    def set_ruta_mal(self, ruta_mal):
        self.ruta_mal = ruta_mal

    def get_ruta_dec(self):
        return self.ruta_dec

    def set_ruta_dec(self, ruta_dec):
        self.ruta_dec = ruta_dec

    def get_ruta_bien(self):
        return self.ruta_bien

    def set_ruta_bien(self, ruta_bien):
        self.ruta_bien = ruta_bien

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_raw_file_d(self):
        return self.raw_file_d

    def set_raw_file_d(self, raw_file_d):
        self.raw_file_d = raw_file_d
        self.blocks_file_sink_2.open(self.raw_file_d)

    def get_raw_file(self):
        return self.raw_file

    def set_raw_file(self, raw_file):
        self.raw_file = raw_file

    def get_pll_alpha(self):
        return self.pll_alpha

    def set_pll_alpha(self, pll_alpha):
        self.pll_alpha = pll_alpha
        self.digital_costas_loop_cc_1_0_1.set_loop_bandwidth(self.pll_alpha)

    def get_lp_taps(self):
        return self.lp_taps

    def set_lp_taps(self, lp_taps):
        self.lp_taps = lp_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.lp_taps)

    def get_lp_corte(self):
        return self.lp_corte

    def set_lp_corte(self, lp_corte):
        self.lp_corte = lp_corte

    def get_loopBW(self):
        return self.loopBW

    def set_loopBW(self, loopBW):
        self.loopBW = loopBW
        self.digital_symbol_sync_xx_0_0_0.set_loop_bandwidth(self.loopBW)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.soapy_source_0.set_gain(0, self.gain)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.analog_sig_source_x_0.set_frequency(self.freq*(1-self.f_real))
        self.soapy_source_0.set_frequency(0, self.freq+self.f_offset)

    def get_f_real(self):
        return self.f_real

    def set_f_real(self, f_real):
        self.f_real = f_real
        self.analog_sig_source_x_0.set_frequency(self.freq*(1-self.f_real))

    def get_f_offset(self):
        return self.f_offset

    def set_f_offset(self, f_offset):
        self.f_offset = f_offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-self.f_offset)
        self.soapy_source_0.set_frequency(0, self.freq+self.f_offset)

    def get_eqGain(self):
        return self.eqGain

    def set_eqGain(self, eqGain):
        self.eqGain = eqGain
        self.digital_cma_equalizer_cc_0.set_gain(self.eqGain)

    def get_debug_2(self):
        return self.debug_2

    def set_debug_2(self, debug_2):
        self.debug_2 = debug_2
        self.blocks_file_sink_0.open(self.debug_2)

    def get_debug_1(self):
        return self.debug_1

    def set_debug_1(self, debug_1):
        self.debug_1 = debug_1

    def get_bitstream_name(self):
        return self.bitstream_name

    def set_bitstream_name(self, bitstream_name):
        self.bitstream_name = bitstream_name

    def get_antenna(self):
        return self.antenna

    def set_antenna(self, antenna):
        self.antenna = antenna
        self.soapy_source_0.set_antenna(0,self.antenna)





def main(top_block_cls=WXsat_LRPT_no_gui, options=None):
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
