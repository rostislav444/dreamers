import {Model3dInterface, ProductInterface} from "@/interfaces/Product";
import {
    CameraImage,
    CameraImagesWrapper,
    GalleryArrowWrapper,
    MainImageWrapper
} from "@/components/App/Product/Galery/style";
import {Box, Image, Grid, GridItem} from "@chakra-ui/react";
import {MEDIA_URL} from "@/local";
import {useState} from "react";
import {CameraImageFromMaterials} from "@/utils/Product/Materials";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";

interface ProductGalleryProps {
    mobile: boolean
    product: ProductInterface,
    selectedMaterials: SelectedMaterialsInterface
}


const getCameraPartsImages = (models3d: Model3dInterface, selectedMaterials: SelectedMaterialsInterface) => {
    return models3d.cameras.map(camera => CameraImageFromMaterials(camera.parts, selectedMaterials))
}


export const ProductGallery = ({mobile, product, selectedMaterials}: ProductGalleryProps) => {
    const imagesBySku: boolean = product.images_by_sku
    const cameras = imagesBySku ? [] : getCameraPartsImages(product.model_3d, selectedMaterials)
    const [currentImage, setCurrentImage] = useState<number>(Math.round(cameras.length / 3))

    const handleContextMenuOpen = (e: any) => {
        if (e.target.tagName.toLowerCase() === 'img') {
            e.preventDefault();
        }
    }

    const handleArrowClick = (direction: number) => {
        if (direction < 0) {
            setCurrentImage(cameras.length - 1)
        } else if (direction >= cameras.length) {
            setCurrentImage(0)
        } else {
            setCurrentImage(direction)
        }
    }

    return <Box w='100%'>
        <MainImageWrapper>
            {cameras[currentImage].map((image, imageKey) =>
                <CameraImage className={'camera-image'} key={imageKey} src={MEDIA_URL + image}/>)}
            <GalleryArrowWrapper
                left={true}
                onClick={() => handleArrowClick(currentImage - 1)}>{'<'}</GalleryArrowWrapper>
            <GalleryArrowWrapper
                left={false}
                onClick={() => handleArrowClick(currentImage + 1)}>{'>'}</GalleryArrowWrapper>
        </MainImageWrapper>

        <Grid mb={4} mr={mobile ? 0 : 20} w={mobile ? '100%' : '80%'} gridTemplateColumns='repeat(6, 1fr)' gap={4}>
            {cameras.map((camera, key) =>
                <GridItem
                    key={key} onClick={() => setCurrentImage(key)}
                    border={currentImage === key ? '2px solid brown' : '2px solid #fff'}
                    _hover={{
                        borderColor: 'beige',
                    }}
                    cursor='pointer'
                >
                    <CameraImagesWrapper onContextMenu={handleContextMenuOpen} key={key}>
                        {camera.map((image, imageKey) => <CameraImage className={'camera-image'} key={imageKey}
                                                                      src={MEDIA_URL + image}/>)}
                    </CameraImagesWrapper>
                </GridItem>
            )}
        </Grid>
    </Box>

}