import React, { Component } from 'react'
import Particles from "react-particles-js";
import axios from 'axios'
import ReactJson from 'react-json-view'
import IMG from './search.png'
import "react-toastify/dist/ReactToastify.css";
import { toast } from "react-toastify";
import { FilePond, registerPlugin } from "react-filepond";
import "filepond/dist/filepond.min.css";
import FilePondPluginImageExifOrientation from "filepond-plugin-image-exif-orientation";
import FilePondPluginImagePreview from "filepond-plugin-image-preview";
import "filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css";
import Annotation from 'react-image-annotation';
import {RectangleSelector} from 'react-image-annotation/lib/selectors'

registerPlugin(FilePondPluginImageExifOrientation, FilePondPluginImagePreview);

export default class App extends Component {

  state = {
    height:0,
    width:0,
    file : undefined,
    loading: false,
    url: 'http://localhost:8000/objects/?key=protected_ai',
    selectedFile: '',
    JsonData: {'Type':'Objects Detection'},
    image:IMG,
    annotations: []
  }

  AlgoRequest = (file) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
        let image = new Image();
        image.src = reader.result;
        this.setState({image : image.src , height:image.height , width:image.width})
    }
    this.setState({ loading: true , selectedFile: file})
    const data = new FormData()
    data.append('file', this.state.selectedFile)
    axios.post(this.state.url, data, {})
      .then(res => {
        this.setState({ JsonData: res.data , loading: false })
        this.makeAnottation(res.data)
        toast.configure();
        toast.error('Completed successfully', {autoClose: 2000});
      }).catch(error => {
        this.setState({ JsonData: JSON.parse(error), selectedFile: '', loading: false })
        toast.configure();
        toast.error({ 'error': 'Somthing went wrong' }, {autoClose: 2000});
      })
  }

  makeAnottation = (results) => {
    let annotations = []
    results.map(v=>{
      let x1 = v.box_points[0]
      let y1 = v.box_points[1]
      let x2 = v.box_points[2]
      let y2 = v.box_points[3]
      let box = {
        geometry:{
          type:RectangleSelector.TYPE,
          x: x1 / this.state.width * 100,
          y: y1 / this.state.height * 100,
          width: ((x2-x1) / this.state.width) * 100 ,
          height: ((y2-y1) / this.state.height) * 100
        },
        data:{
          text:v.name +':'+v.percentage_probability.toFixed(4),
          id:x1+y2+x2
        }
      }
      annotations.push(box)
      return 'seccessfully'
    })
    this.setState({annotations})
}
 
  render() {
    return (
      <div>
        <Particles
          className="Particles"
          params={{ particles: { number: { value: 200, density: { enable: true, value_area: 5000, }, }, }, }}
        />
        {this.state.loading ? <div className="loading-page"><div className='loader' /></div> : ''}
        <div className='main-flex'>
          <div className='form-main'>
            <FilePond
                        allowMultiple={false}
                        allowReplace={false}
                        onaddfile={(err, file) => {
                            const reader = new FileReader();
                            reader.readAsDataURL(file.file);
                            reader.onload = () => {
                                let image = new Image();
                                image.src = reader.result;
                                image.onload = () => {this.AlgoRequest(file.file)}};
                        }}
                        onremovefile={(err, file) => {
                          this.setState({selectedFile:'' , annotations:[] ,  JsonData:{'Algorithm':'Objects Detection'}, image:IMG , anotations:[]})
                      }}
                        />
            <ReactJson displayDataTypes={false} indentWidth={3} iconStyle={"circle"} src={this.state.JsonData} />
          </div>
          <div className='annotation-main'>
          <Annotation
            src={this.state.image}
            annotations={this.state.annotations}
            value={{}}
            disableOverlay={true}
            />
          </div>
        </div>
      </div>
    )
  }
}