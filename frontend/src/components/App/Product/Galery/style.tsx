import styled from '@emotion/styled'


export const MainImageWrapper = styled.div`
    position: relative;
    display: block;
    width: 100%;
    height: auto;
    padding-top: calc(100% / 3 * 2);
`

export const CameraImagesWrapper = styled.div`
    position: relative;
    display: block;
    width: 100%;
    height: auto;
    padding-top: calc(100% / 3 * 2);
`


export const CameraImage = styled.img`
    image-rendering: pixelated;
    position: absolute;
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    top: 0;
`


export const GalleryArrowWrapper = styled.div<{ left: boolean }>`
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    top: 50%;
    right: ${props => props.left ? 'auto' : '0'};
    cursor: pointer;
    padding: 4px;
    width: 48px;
    height: 48px;
    transition: background-color 0.3s;
    z-index: 1000;

    &:hover {
        background-color: rgba(255, 255, 255, 0.7);
    }
`