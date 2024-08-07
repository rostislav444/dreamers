import {Model3dInterface, ProductInterface} from "@/interfaces/Product";
import {
    CameraImage,
    CameraImagesWrapper,
    GalleryArrowWrapper,
    MainImageWrapper
} from "@/components/App/Product/Galery/style";
import {Box, Grid, GridItem, IconButton} from "@chakra-ui/react";
import {MEDIA_URL} from "@/local";
import {useState} from "react";
import {CameraImageFromMaterials} from "@/utils/Product/Materials";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import mergeImages from 'merge-images';
import {saveAs} from 'file-saver';
import {DownloadIcon} from "@chakra-ui/icons";

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
    const [mergedImage, setMergedImage] = useState<any>(null);

    // console.log('cameras', cameras)

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

    const handleImageMergeAndDownload = async (images: string[]) => {
        try {
            const imageBlobs = await Promise.all(images.map(async (image) => {
                const response = await fetch(MEDIA_URL + image);
                const blob = await response.blob();
                return URL.createObjectURL(blob);
            }));

            const merged = await mergeImages(imageBlobs);
            // Конвертируем base64 в Blob
            const byteString = atob(merged.split(',')[1]);
            const mimeString = merged.split(',')[0].split(':')[1].split(';')[0];
            const ab = new ArrayBuffer(byteString.length);
            const ia = new Uint8Array(ab);
            for (let i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }
            const blob = new Blob([ab], {type: mimeString});

            // Генерация рандомного имени файла
            const randomFileName = `dreamers-${Math.random().toString(36).substr(2, 9)}.png`;

            // Скачивание файла
            saveAs(blob, randomFileName);
        } catch (error) {
            console.error('Error merging images:', error);
        }
    };


    return <Box w='100%'>
        <MainImageWrapper>
            {cameras[currentImage].map((image, imageKey) =>
                <CameraImage className={'camera-image'} key={imageKey} src={MEDIA_URL + image.image}/>)}
            <GalleryArrowWrapper
                left={true}
                onClick={() => handleArrowClick(currentImage - 1)}>{'<'}</GalleryArrowWrapper>
            <GalleryArrowWrapper
                left={false}
                onClick={() => handleArrowClick(currentImage + 1)}>{'>'}</GalleryArrowWrapper>

            {/*<IconButton aria-label='download' icon={<DownloadIcon color='brown.500'/>} position='absolute' top='4' right='4'*/}
            {/*            onClick={() => handleImageMergeAndDownload(cameras[currentImage].image)}*/}
            {/*            variant='ghost'*/}
            {/*/>*/}

        </MainImageWrapper>

        {/*{mergedImage && <Image src={mergedImage}/>}*/}


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
                        {camera.map((image, imageKey) => {
                            return <CameraImage className={'camera-image'} key={imageKey} src={MEDIA_URL + image.thumbnails.s}/>
                        })}
                    </CameraImagesWrapper>
                </GridItem>
            )}
        </Grid>
    </Box>

}