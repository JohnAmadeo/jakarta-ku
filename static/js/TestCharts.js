import React from 'react';
import ReactDOM from 'react-dom'
import Store from 'store2';
import Request from 'superagent';
import Axios from 'axios';
import Utils from './utils';

import Graphic from './Graphic';

const TestBarList = (props) => {
  return (
    <div>
    <Graphic chartName={'Jumlah Orang per Status Pendidikan'}
             chartType={'bar'}
             dataFields={{
               values: [10,20,30,40,50,60, 10,20,30,40,50,60],
               labels: ['Excellent Performance', 
                        'Good Performance',
                        'Satisfactory Performance',
                        'Below Average Performance', 
                        'Insufficient Performance',
                        'Performance not recorded',
                        'Excellent Performance', 
                        'Good Performance',
                        'Satisfactory Performance',
                        'Below Average Performance', 
                        'Insufficient Performance',
                        'Performance not recorded']   
             }}
             dataOptions={{
               fieldAxis: 'Nilai',
               measureAxis: 'Jumlah Orang',
               tooltipStringFormat: ['_', 'Orang']
             }}/>
    <Graphic chartName={'Jumlah Orang per Status Pendidikan Title Panjang'}
             chartType={'bar'}
             dataFields={{
               values: [10,20],
               labels: ['Excellent Performance', 
                        'Good Performance']   
             }}
             dataOptions={{
               fieldAxis: 'Nilai',
               measureAxis: 'Jumlah Orang',
               tooltipStringFormat: ['_', 'Orang']
             }}/>
    <Graphic chartName={'Jumlah Orang per Status Pendidikan'}
             chartType={'bar'}
             dataFields={{
               values: [10,20,30],
               labels: ['Excellent Performance', 
                        'Good Performance',
                        'Sufficient Performance']   
             }}
             dataOptions={{
               fieldAxis: 'Nilai',
               measureAxis: 'Jumlah Orang',
               tooltipStringFormat: ['_', 'Orang']
             }}/>
    <Graphic chartName={'Jumlah Orang per Status Pendidikan Title Panjang'}
             chartType={'bar'}
             dataFields={{
               values: [10,20],
               labels: ['Excellent Performance', 
                        'Good Performance']   
             }}
             dataOptions={{
               fieldAxis: 'Nilai',
               measureAxis: 'Jumlah Orang',
               tooltipStringFormat: ['_', 'Orang']
             }}/>                 
    <Graphic chartName={'Jumlah Orang per Status Pendidikan'}
             chartType={'bar'}
             dataFields={{
               values: [10,20,30,40],
               labels: ['Excellent Performance', 
                        'Good Performance',
                        'Sufficient Performance',
                        'Poor Performance']   
             }}
             dataOptions={{
               fieldAxis: 'Nilai',
               measureAxis: 'Jumlah Orang',
               tooltipStringFormat: ['_', 'Orang']
             }}/>
    <Graphic chartName={'Jumlah Orang per Status Pendidikan'}
             chartType={'bar'}
             dataFields={{
               values: [10,20,30,40,50],
               labels: ['Excellent Performance', 
                        'Good Performance',
                        'Sufficient Performance',
                        'Poor Performance',
                        'Performance Not Recorded']   
             }}
             dataOptions={{
               fieldAxis: 'Nilai',
               measureAxis: 'Jumlah Orang',
               tooltipStringFormat: ['_', 'Orang']
             }}/> 
    <Graphic chartName={'Jumlah Orang per Status Pendidikan'}
             chartType={'bar'}
             dataFields={{
               values: [10,20,30,40,50, 60],
               labels: ['Excellent Performance', 
                        'Good Performance',
                        'Sufficient Performance',
                        'Poor Performance',
                        'Performance Not Recorded',
                        'Performance Lost']   
             }}
             dataOptions={{
               fieldAxis: 'Nilai',
               measureAxis: 'Jumlah Orang',
               tooltipStringFormat: ['_', 'Orang']
             }}/>   
    </div>
  )
}

const TestDoughnutList = (props) => {
  return (
    <div>
      <Graphic chartName={'Jumlah Orang per Status Pendidikan'}
               chartType={'doughnut'}
               dataFields={{
                 values: [10,20,30,40,50,60,10,20,30,40,50,60],
                 labels: ['Excellent Performance', 
                          'Good Performance',
                          'Satisfactory Performance',
                          'Below Average Performance', 
                          'Insufficient Performance',
                          'Performance not recorded',
                          'Excellent Performance', 
                          'Good Performance',
                          'Satisfactory Performance',
                          'Below Average Performance', 
                          'Insufficient Performance',
                          'Performance not recorded']   
               }}
               dataOptions={{
                 fieldAxis: 'Nilai',
                 measureAxis: 'Jumlah Orang',
                 tooltipStringFormat: ['_', 'Orang']
               }}/> 
      <Graphic chartName={'Jumlah Orang per Status Pendidikan'}
               chartType={'doughnut'}
               dataFields={{
                 values: [10,20,30],
                 labels: ['Excellent Performance', 
                          'Good Performance',
                          'Satisfactory Performance']   
               }}
               dataOptions={{
                 fieldAxis: 'Nilai',
                 measureAxis: 'Jumlah Orang',
                 tooltipStringFormat: ['_', 'Orang']
               }}/>
      <Graphic chartName={'Jumlah Orang per Status Pendidikan'}
               chartType={'doughnut'}
               dataFields={{
                 values: [10,20,30,40,50,60,10,20,30,40,50,60],
                 labels: ['Excellent Performance', 
                          'Good Performance',
                          'Satisfactory Performance',
                          'Below Average Performance', 
                          'Insufficient Performance',
                          'Performance not recorded',
                          'Excellent Performance', 
                          'Good Performance',
                          'Satisfactory Performance',
                          'Below Average Performance', 
                          'Insufficient Performance',
                          'Performance not recorded']   
               }}
               dataOptions={{
                 fieldAxis: 'Nilai',
                 measureAxis: 'Jumlah Orang',
                 tooltipStringFormat: ['_', 'Orang']
               }}/> 
      <Graphic chartName={'Jumlah Orang per Status Pendidikan'}
               chartType={'doughnut'}
               dataFields={{
                 values: [10,20,30],
                 labels: ['Excellent Performance', 
                          'Good Performance',
                          'Satisfactory Performance']   
               }}
               dataOptions={{
                 fieldAxis: 'Nilai',
                 measureAxis: 'Jumlah Orang',
                 tooltipStringFormat: ['_', 'Orang']
               }}/>
    </div>
  )
}

module.exports = {
  TestBarList,
  TestDoughnutList
}