import styled from '@emotion/styled'


export const CameraImagesWrapper = styled.div`
  position: relative;
  display: block;
  width: 100%;
  height: auto;
  padding-top: calc(100% / 3 * 2);
  background-color: white;
`


export const CameraImage = styled.img`
  position: absolute;
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  top: 0;
`