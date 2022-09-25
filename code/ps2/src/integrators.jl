export VelocityVerlet
export take_one_step!

abstract type Integrator end
struct VelocityVerlet <: Integrator end

function take_one_step!(particles, i, Δt, ::VelocityVerlet)
    particle = particles[i]
    particle.v += acceleration(particles)(i) * Δt / 2  # 𝐯(t + Δt / 2)
    particle.r += particle.v * Δt  # 𝐫(t + Δt)
    𝐚 = acceleration(particles)(i)  # 𝐚(t + Δt)
    particle.v += 𝐚 * Δt / 2  # 𝐯(t + Δt)
    return particles
end
function take_one_step!(particles, Δt, ::VelocityVerlet)
    for i in eachindex(particles)
        take_one_step!(particles, i, Δt, ::VelocityVerlet)
    end
    return particles
end
