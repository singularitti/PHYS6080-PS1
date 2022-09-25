using StaticArrays: SVector, MVector

export Particle
export distance, potential_energy, acceleration, distribute!, initialize!

const ε = 120
const σ = 0.34
const ρ = 0.75

mutable struct Particle
    r::MVector{3,Float64}
    v::MVector{3,Float64}
    Particle() = new()  # Incomplete initialization
end

function distance(particle1::Particle, particle2::Particle)
    return sqrt(sum(abs2, particle1.r - particle2.r))
end

function potential_energy(particle1::Particle, particle2::Particle)
    r = distance(particle1, particle2)
    η = 1 / r^6
    return 4ε * η * (η - 1)
end
function potential_energy(particles)
    total = 0
    for (i, particleᵢ) in enumerate(particles)
        for particleⱼ in particles[i:end]
            total += potential_energy(particleᵢ, particleⱼ)
        end
    end
    return 2total
end

struct Acceleration
    particle::Particle
end
function (𝐚::Acceleration)(particle2::Particle)
    particle1 = 𝐚.particle
    η = 1 / distance(particle1, particle2)
    if distance(particle1, particle2) == 0
        return zeros(MVector{3,Float64})
    end
    return (particle1.r - particle2.r) * (η^14 - η^8)
end
function (𝐚::Acceleration)(particles)
    @assert length(particles) > 1 "you must have more than 1 particle to calculate the force!"
    @assert 𝐚.particle ∉ particles
    return sum(𝐚, particles)
end

acceleration(particle::Particle) = Acceleration(particle)
function acceleration(particles)
    return map(eachindex(particles)) do i
        sum(
            acceleration(particles[i])(particles[filter(j -> j != i, eachindex(particles))])
        )
    end
end

function distribute!(particles, volume)
    n = length(particles)
    @assert n > 0
    a = cbrt(volume)
    for (particle, coordinates) in zip(particles, eachcol(a * rand(3, n)))
        particle.r = coordinates
    end
    @assert unique(particles) == particles
    return particles
end

function initialize!(particles)
    @assert length(particles) > 0
    for particle in particles
        particle.v = zeros(MVector{3,Float64})
    end
    return particles
end
