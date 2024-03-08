import {Model3dInterface, ProductInterface} from "@/interfaces/Product";
import {selectedMaterialsInterface} from "@/components/App/Product";
import {CameraImage, CameraImagesWrapper} from "@/components/App/Product/Galery/style";
import {Box} from "@chakra-ui/react";


interface ProductGalleryProps {
    mobile: boolean
    product: ProductInterface,
    selectedMaterials: selectedMaterialsInterface
}


const getCameraPartsImages = (models3d: Model3dInterface, selectedMaterials: selectedMaterialsInterface) => {
    return models3d.cameras.map(camera =>
        camera.parts.map(part =>
            part.materials.find(material => material.material == selectedMaterials[part.part.id])?.image
        ).reverse()
    )
}


export const ProductGallery = ({mobile, product, selectedMaterials}: ProductGalleryProps) => {
    const imagesBySku: boolean = product.images_by_sku
    const cameras = imagesBySku ? [] : getCameraPartsImages(product.model_3d, selectedMaterials)

    const handleContextMenuOpen = (e: any) => {
        if (e.target.tagName.toLowerCase() === 'img') {
            e.preventDefault();
        }
    }

    return <Box mb={4} mr={mobile ? 0 : 20} w={mobile ? '100%' : '80%'}>{
        cameras.map((camera, key) =>
            <CameraImagesWrapper onContextMenu={handleContextMenuOpen} key={key}>
                {camera.map((image, imageKey) => <CameraImage className={'camera-image'} key={imageKey} src={image}/>)}
            </CameraImagesWrapper>
        )
    }</Box>
}