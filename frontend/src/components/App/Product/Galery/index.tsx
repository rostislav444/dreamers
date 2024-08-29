import {Model3dInterface, ProductInterface} from "@/interfaces/Product";
import {
    CameraImage,
    CameraImagesWrapper,
    GalleryArrowWrapper,
    MainImageWrapper
} from "@/components/App/Product/Galery/style";
import {Box, Flex, Grid, GridItem, Heading, IconButton, Image} from "@chakra-ui/react";

import {BASE_URL, MEDIA_URL} from "@/local";
import {useState} from "react";
import {CameraImageFromMaterials} from "@/utils/Product/Materials";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {ChevronUpIcon, DownloadIcon} from "@chakra-ui/icons";
import {handleImageMergeAndDownload} from "@/components/App/Product/Galery/utils";

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
    const [selectedInterior, setSelectedInterior] = useState<any[]>([null, null])
    const [showInterior, setShowInterior] = useState<boolean>(true)

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


    const interiors = product.model_3d.cameras[currentImage].interior_layers.map(
        (layer, i) => {
            return layer.materials[selectedInterior[i]]?.image
        }
    ).filter(Boolean)

    const images = [...cameras[currentImage].map(
        image => `${MEDIA_URL}${mobile ? image.thumbnails.m : image.image}`), ...interiors,]

    const handleSelectedInterior = (key: number, materialKey: number | null) => {
        const newSelectedInterior = [...selectedInterior]
        newSelectedInterior[key] = materialKey
        setSelectedInterior(newSelectedInterior)
    }


    return <Box w='100%'>
        <MainImageWrapper>
            {images.map((image: string, imageKey: number) =>
                <CameraImage className={'camera-image'} key={imageKey}
                             src={image}/>)}
            <GalleryArrowWrapper
                left={true}
                onClick={() => handleArrowClick(currentImage - 1)}>{'<'}</GalleryArrowWrapper>
            <GalleryArrowWrapper
                left={false}
                onClick={() => handleArrowClick(currentImage + 1)}>{'>'}</GalleryArrowWrapper>
            <IconButton aria-label='download' icon={<DownloadIcon color='brown.500'/>} position='absolute' top='4'
                        right='4'
                        onClick={() => handleImageMergeAndDownload(images)}
                        variant='ghost'
            />
        </MainImageWrapper>


        <Grid mt={2} mb={4} mr={mobile ? 0 : 20} w={mobile ? '100%' : '80%'}
              gridTemplateColumns={mobile ? 'repeat(auto-fill, minmax(60px, 1fr))' : 'repeat(auto-fill, minmax(80px, 1fr))'}
              gap={2}>
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
                        {camera.map((image, imageKey) => {
                            return <CameraImage className={'camera-image'} key={imageKey}
                                                src={MEDIA_URL + image.thumbnails.s}/>
                        })}
                    </CameraImagesWrapper>
                </GridItem>
            )}
        </Grid>

        <Box>
            <Flex justifyContent='space-between' alignItems='center' onClick={() => setShowInterior(!showInterior)}>
                <Heading size='md'>Інтер&apos;ер</Heading>
                <ChevronUpIcon w='6' h='6' color='brown.500' cursor='pointer'
                               transform={showInterior ? 'rotate(180deg)' : 'rotate(0deg)'}
                />
            </Flex>
            {showInterior && <Box mt='4'>
                {product.model_3d.cameras[currentImage].interior_layers.map((layer, key) => {
                    return <Grid gridTemplateColumns={mobile ?
                        'repeat(auto-fill, minmax(60px, 1fr))' :
                        'repeat(auto-fill, minmax(100px, 1fr))'
                    } gap={2} mb='2' key={key}>
                        <Box borderWidth='2px' borderColor={selectedInterior[key] === null ? 'brown.500' : 'white'}
                             onClick={() => handleSelectedInterior(key, null)}/>
                        {layer.materials.map((material, materialKey) => {
                            return <Box borderWidth='2px' key={materialKey}
                                        borderColor={selectedInterior[key] === materialKey ? 'brown.500' : 'white'}>
                                <Image onClick={() => handleSelectedInterior(key, materialKey)}
                                       key={materialKey} src={material.image}/>
                            </Box>

                        })}
                    </Grid>
                })}
            </Box>}
        </Box>
    </Box>

}